import datetime

from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from projectmanager.models import Project, ProjectTime, ProjectExpense, Task, \
    Organisation, OrganisationUser, Invoice, InvoiceRow


class ProjectExpenseInline(admin.TabularInline):
    model = ProjectExpense
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        return qs.annotate(latest_time=models.Max('projecttime__start'))

    def save_model(self, req, obj, *args, **kwargs):
        obj.owner = req.user
        return super(ProjectAdmin, self).save_model(req, obj, *args, **kwargs)

    list_display = ('client', 'name', 'total_hours', 'invoiceable_hours',
                    'invoiced_hours', 'latest_time', 'to_invoice', 'links', )
    list_display_links = ('client', 'name')
    list_filter = ('archived', 'created', 'client', )
    search_fields = ('name', 'client__name', 'description')
    inlines = [ProjectExpenseInline, TaskInline, ]
    actions = ['create_invoice_for_selected', ]
    exclude = ('owner', )

    def links(self, obj):
        time_url = reverse('admin:projectmanager_projecttime_changelist')
        return (u'<a href="%s?task__project__id__exact=%s">view</a> ' %
                (time_url, obj.pk)) + \
               (u'<a href="%s">csv</a> ' % obj.projecttime_summary_url())

    def create_invoice_for_selected(self, request, queryset):
        invoice = Invoice.objects.create()
        invoice.create_rows(projects=queryset)
        url = reverse('admin:projectmanager_invoice_change',
                      args=(invoice.id,))
        return HttpResponseRedirect(url)

    links.short_description = ' '
    links.allow_tags = True

admin.site.register(Project, ProjectAdmin)


class ProjectTimeAdmin(admin.ModelAdmin):
    list_display = ('project', 'description', 'start', 'end', 'total_time')
    list_filter = ('start', 'task__project', )
    search_fields = ('description',)
    date_hierarchy = 'start'
    raw_id_fields = ('task', )

admin.site.register(ProjectTime, ProjectTimeAdmin)


class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 2
    raw_id_fields = ('task',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'description', 'created_display',
                    'subtotal', 'paid', 'invoice')
    list_filter = ('created', 'paid')
    inlines = [InvoiceRowInline]
    actions = ['make_paid']
    search_fields = ['client', 'email', 'description', 'address']

    def queryset(self, request):
        qs = super(InvoiceAdmin, self).queryset(request)
        qs = qs.annotate(quantity_sum=models.Sum('invoicerow__quantity'))
        return qs

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.admin_order_field = 'subtotal_order'

    def make_paid(self, request, queryset):
        queryset.update(paid=True)

    def created_display(self, instance):
        return datetime.date(instance.created.year, instance.created.month, instance.created.day)
    created_display.admin_order_field = 'created'

    def invoice(self, instance):
        return u'<a href="/invoice/%d/%s">pdf</a>' % (instance.id, instance.pdf_filename()) + u' | <a href="/invoice/%d/">html</a>' % (instance.id)

    invoice.allow_tags = True

admin.site.register(Invoice, InvoiceAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_filter = ('completed', 'created', )
    list_display = ('project', 'task', 'total_hours', 'invoiceable_hours',
                    'invoiced_hours', 'when_completed', )
    search_fields = ('project__name', 'task')
    raw_id_fields = ('project',)

    def when_completed(self, obj):
        return obj.completion_date.date() if obj.completed else ''
    when_completed.admin_order_field = 'completed'
    when_completed.short_description = 'Completed'

admin.site.register(Task, TaskAdmin)


class OrganisationUserInline(admin.TabularInline):
    model = OrganisationUser
    extra = 1
    raw_id_fields = ('user', )

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users', )
    inlines = [OrganisationUserInline]

    def get_users(self, obj):
        return ', '.join(u.get_full_name() for u in obj.users.all())
    get_users.short_description = 'users'

admin.site.register(Organisation, OrganisationAdmin)
