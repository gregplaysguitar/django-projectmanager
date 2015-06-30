import datetime, decimal
import hashlib
import calendar

from django.db import models
from django.db.models import F
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.db.models.signals import pre_save, post_save, post_init
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from . import settings as pm_settings


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0] + suffix


def cache_key(obj, func_name, *args, **kwargs):
    key = [settings.CACHE_MIDDLEWARE_KEY_PREFIX,
           func_name,
           obj._meta.app_label,
           obj._meta.model_name,
           str(obj.pk)]
    for extra in (args, kwargs):
        if len(extra):
            key.append(hashlib.sha1(str(extra)).hexdigest()[:8])
    return '-'.join(key)


def cached_method(duration=86400):
    def decorator(func):
        def inner(obj, *args, **kwargs):
            key = cache_key(obj, func.__name__, *args, **kwargs)
            result = cache.get(key)
            if result == None:
                result = func(obj, *args, **kwargs)
                cache.set(key, result, duration)
            return result
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        return inner
    return decorator


def default_manager_from_qs(qs_cls, **kwargs):
    related = kwargs.pop('use_for_related_fields', True)
    class _Manager(models.Manager.from_queryset(qs_cls)):
        use_for_related_fields = related
    return _Manager


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, default='')
    
    def __unicode__(self):
        return self.name


class ProjectQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(users=user) | Q(owner=user))


class Project(models.Model):
    owner = models.ForeignKey(User, related_name='project_ownership_set')
    users = models.ManyToManyField(User, related_name='project_membership_set', 
                                   blank=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(db_index=True)
    hidden = models.BooleanField(db_index=True)
    billable = models.BooleanField(default=1, db_index=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, 
                                      default=pm_settings.HOURLY_RATE)
    creation_date = models.DateTimeField(auto_now_add=True)
    billing_type = models.CharField(max_length=5, choices=(('quote', 'Quote'), 
                                                           ('time', 'Time'),), 
                                    default='quote')
    
    objects = default_manager_from_qs(ProjectQuerySet)()
    
    def __unicode__(self):
        if self.client:
            return "%s, %s" % (self.name, self.client)
        else:
            return self.name
    
    def clear_cache(self):
        for name in ('total_hours', 'invoiceable_hours', 'invoiced_hours'):
            cache.delete(cache_key(self, name))
    
    def get_projecttime(self):
        return ProjectTime.objects.filter(task__project=self)
    
    def pending_tasks(self):
        return self.task_set.filter(completed=False)
    
    @cached_method()
    def total_hours(self):
        return sum(t.total_hours() for t in self.task_set.all())
    
    @cached_method()
    def invoiceable_hours(self):
        tasks = self.task_set.all()
        return sum(t.invoiceable_hours() for t in tasks)
    
    @cached_method()
    def invoiced_hours(self):
        tasks = self.task_set.all()
        return sum(t.invoiced_hours() for t in tasks)
    
    @cached_method()
    def latest_time(self):
        try:
            projecttime = self.get_projecttime().order_by('-start')[0]
        except IndexError:
            return None
        else:
            return projecttime.start.date()
    latest_time.admin_order_field = 'task__projecttime__start'
    
    # @cached_method()
    # def total_estimated_hours(self, completed=False):
    #     tasks = self.task_set.all()
    #     if completed:
    #         tasks = tasks.filter(completed=True)
    #     return tasks.aggregate(Sum('estimated_hours'))['estimated_hours__sum'] or ''
    # 
    # total_estimated_hours.short_description = 'Est. hours'
    # 
    # @cached_method()
    # def total_expenses(self):
    #     return float(sum(item.amount for item in ProjectExpense.objects.filter(project=self.id)))
    # 
    # @cached_method() 
    # def time_invoiced(self):
    #     return float(sum(item.quantity for item in InvoiceRow.objects.filter(project=self) if item.is_time))
    # time_invoiced.short_description = 'Hours'
    # 
    # @cached_method()
    # def total_invoiced(self):
    #     return float(sum(item.amount() for item in InvoiceRow.objects.filter(project=self)))
    # total_invoiced.short_description = 'Invoiced'
    # 
    # @cached_method()
    # def total_cost(self):
    #     if self.billing_type == 'quote':
    #         return self.total_expenses() + float(self.total_estimated_hours(True) or 0) * float(self.hourly_rate)
    #     else:
    #         return self.total_expenses() + self.total_time() * float(self.hourly_rate)
    # 
    # @cached_method()
    # def total_to_invoice(self):
    #     return max(0, self.total_cost() - self.total_invoiced())
    # total_to_invoice.short_description = 'To invoice'
    # 
    # @cached_method()
    # def approx_hours_to_invoice(self):
    #     if self.hourly_rate:
    #         return str(round(int(self.total_to_invoice() * 4) / self.hourly_rate) / 4)
    #     else:
    #         return ''
    # approx_hours_to_invoice.short_description = 'Hours'
    
    
    @models.permalink
    def projecttime_summary_url(self):
        return ('projectmanager.views.projecttime_summary', (self.pk, ), )
    
    class Meta:
        ordering = ('name',)

def clear_project_cache(sender, instance, **kwargs):
    if isinstance(instance, Project):
        instance.clear_cache()    
    elif hasattr(instance, 'project') and isinstance(instance.project, Project):
        instance.project.clear_cache()
post_save.connect(clear_project_cache)


class ForProjectUserQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(project__users=user) | Q(project__owner=user))

ForProjectUserManager = default_manager_from_qs(ForProjectUserQuerySet)


class Task(models.Model):
    project = models.ForeignKey(Project)
    task =  models.TextField()
    comments = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, editable=False)
    quoted_hours = models.DecimalField(max_digits=5, decimal_places=2, 
                                          default=0, null=True, blank=True)

    objects = ForProjectUserManager()
    
    def total_hours(self):
        return ProjectTime.objects.filter(task=self) \
                          .aggregate(total=models.Sum('_hours'))['total'] or 0
    
    def invoiceable_hours(self):
        """Quoted tasks are billed on completion; non-quoted are billed as 
           they go. 
           TODO do we need a "bill on completion" option? """
        
        if self.quoted_hours:
            return self.quoted_hours if self.completed else 0
        else:
            return self.total_hours()    
    
    def invoiced_hours(self):
        return InvoiceRow.objects.filter(task=self) \
                         .aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @models.permalink
    def get_absolute_url(self):
        return ('projectmanager.views.tasks',)

    def __unicode__(self):
        return "%s: %s" % (self.project.name, self.task)

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)

    class Meta:
        ordering = ('creation_date',)


class ProjectTimeQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(task__project__users=user) | \
                           Q(task__project__owner=user))


def round_datetime(dt):
    minutes = round((dt.minute + float(dt.second) / 60) / 15) * 15 - dt.minute
    return dt + datetime.timedelta(minutes=minutes, seconds=-dt.second)


class ProjectTime(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    description = models.TextField(blank=True, default='')
    # project = models.ForeignKey(Project)
    task = models.ForeignKey(Task)
    _hours = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    
    objects = default_manager_from_qs(ProjectTimeQuerySet)()
    
    @property
    def project(self):
        return self.task.project
    
    def description_truncated(self):
        return smart_truncate(self.description, 100)
    
    def __unicode__(self):
        return "%s: %s (%s)" % (self.project.name, self.description, unicode(self.start))
    
    def total_time(self):
        return (self.end - self.start)

    def save(self, force_insert=False, force_update=False, using=None):
        self.start = round_datetime(self.start)
        self.end = round_datetime(self.end)
        
        hours = self.total_time().days * 24 + self.total_time().seconds / 3600
        part_hours = ((0.0 + self.total_time().seconds / 60) % 60) / 60
        self._hours = str(hours + part_hours)

        super(ProjectTime, self).save(force_insert, force_update, using)



class ProjectExpense(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    project = models.ForeignKey(Project)
    
    objects = ForProjectUserManager()
    
    def description_truncated(self):
        return smart_truncate(self.description, 30)
    
    def __unicode__(self):
        return "%s: %s (%s)" % (self.project.name, self.description, self.amount)


class Invoice(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    paid = models.BooleanField(db_index=True)
    # projects = models.ManyToManyField(Project, through="InvoiceRow")
    
    objects = ForProjectUserManager()
    
    def invoice_summary(self):
        '''Return invoice rows summarized by project.'''
        return self.invoicerow_set.order_by('task__project__name') \
                   .values('task__project__name', 'price') \
                   .annotate(amount=models.Sum(F('quantity') * F('price'))) \
                   .annotate(q_sum=models.Sum('quantity'))
    
    def pdf_filename(self):
        return "Invoice %s - %s - %s.pdf" % (self.creation_date.strftime("%Y-%m-%d"), self.client, self.description)
    
    def __unicode__(self):
        return '%s: %s' % (self.client, self.description)

    def subtotal(self):
        return sum(float(row.amount()) for row in self.invoicerow_set.all())
    
    def gst_amount(self):
        return (float(self.subtotal()) * pm_settings.SALES_TAX)
    
    def total(self):
        return (float(self.subtotal()) * (1 + pm_settings.SALES_TAX))
    
    @models.permalink
    def get_absolute_url(self):
        return ('projectmanager.views.invoice', [self.pk])


def create_invoice_for_projects(project_qs):
    new_invoice = Invoice(paid=False)
    for project in  project_qs.exclude(client__isnull=True)[:1]:
        new_invoice.email = project.client.email
        new_invoice.client = project.client.name
    new_invoice.save()

    for project in project_qs.all():
        for task in Task.objects.filter(project=project, completed=True):
            to_invoice = task.invoiceable_hours() - task.invoiced_hours()
            if to_invoice:
                InvoiceRow.objects.create(
                    invoice=new_invoice,
                    task=task,
                    detail='',
                    quantity=to_invoice,
                    price=project.hourly_rate,
                )
    
    return new_invoice


class InvoiceRow(models.Model):
    task = models.ForeignKey(Task)
    invoice = models.ForeignKey(Invoice)
    detail = models.CharField(max_length=255, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('task__project__name', 'task__task')
    
    def amount(self):
        return (self.price * self.quantity)

    def __unicode__(self):
        created = self.invoice.creation_date.strftime('%d/%m/%Y')
        return "%s on %s (%s)" % (self.amount(), self.task.task, created)
        
    # @property
    # def is_time(self):
    #     return (self.price == self.project.hourly_rate)

    def invoice_date(self):
        return datetime.date(self.invoice.creation_date.year, self.invoice.creation_date.month, self.invoice.creation_date.day)
