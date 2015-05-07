import datetime, decimal

from django.db import models
from django.core.cache import cache
from django.db.models.signals import pre_save, post_save, post_init
from django.contrib.auth.models import User
from django.db.models import Sum

from projectmanager.models import InvoiceRow, Invoice, smart_truncate, \
                                  cached_method, cache_key


BILLING_PERIOD_MONTHS_CHOICES = (
    ('6', '6 monthly',),
    ('12', 'Yearly'),
)
BILLING_PERIOD_MONTHS_DEFAULT = '12'


class HostingClient(models.Model):
    owner = models.ForeignKey(User, related_name='hosting_client_ownership_set', default=1)
    users = models.ManyToManyField(User, related_name='hosting_client_membership_set', blank=True)
    client = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=60, unique=True)
    billing_frequency = models.CharField(u'billing type', editable=False, max_length=10, choices=BILLING_PERIOD_MONTHS_CHOICES, default=BILLING_PERIOD_MONTHS_DEFAULT)
    billing_period = models.CharField(max_length=10, editable=False, default='month')
    period_fee = models.DecimalField(max_digits=10, decimal_places=2, default=25)
    start_date = models.DateField(default=datetime.date.today)
    invoice_rows = models.ManyToManyField(InvoiceRow, through='HostingInvoiceRow')
    
    invoice_due = models.BooleanField(db_column='invoice_due', editable=False)
    def _invoice_due(self):
        #print (self.total_paid < self.total_cost), (self.total_paid, self.total_cost)
        return (self.total_invoiced() <= self.total_cost())
    
    termination_date = models.DateField(null=True, blank=True)
    
    hidden = models.BooleanField(default=False, editable=False)
    def _hidden(self):
        return bool(self.termination_date and self.termination_date < datetime.date.today())

    @cached_method()
    def total_expenses(self):
        return sum(item.amount for item in self.hostingexpense_set.filter(writeoff=False))
        
    @cached_method()
    def total_cost(self):
        if self.termination_date:
            end = self.termination_date
        else:
            end = datetime.date.today()
        months = end.month - self.start_date.month + (end.year - self.start_date.year) * 12
        return self.total_expenses() + months * self.period_fee
    
    @cached_method()
    def total_paid(self):
        return sum(r.amount() for r in self.invoice_rows.filter(invoice__paid=True))

    @cached_method()
    def total_invoiced(self):
        return sum(r.amount() for r in self.invoice_rows.all())
        
    def clear_cache(self):
        for name in ('total_expenses', 'total_cost', 'total_paid', 'total_invoiced'):
            cache.delete(cache_key(self, name))
        
    def __unicode__(self):
        return "%s - %s" % (self.client, self.name)
    

def hostingclient_prefill(sender, *args, **kwargs):
    if kwargs['instance'].pk:
        kwargs['instance'].invoice_due = kwargs['instance']._invoice_due()
        kwargs['instance'].hidden = kwargs['instance']._hidden()
        
pre_save.connect(hostingclient_prefill, sender=HostingClient)
post_init.connect(hostingclient_prefill, sender=HostingClient)

def clear_hostingclient_cache(sender, instance, **kwargs):
    if isinstance(instance, HostingClient):
        instance.clear_cache()    
    elif hasattr(instance, 'hosting_client') and isinstance(instance.hosting_client, HostingClient):
        instance.hosting_client.clear_cache()
post_save.connect(clear_hostingclient_cache)


class HostingInvoiceRow(models.Model):
    hosting_client = models.ForeignKey(HostingClient)
    invoicerow = models.ForeignKey(InvoiceRow)
    is_hosting = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s, %s: $%s" % (self.hosting_client.client, self.hosting_client.name, self.invoicerow.amount())
        

class HostingExpense(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    hosting_client = models.ForeignKey(HostingClient)
    writeoff = models.BooleanField(default=False)

    
    def description_truncated(self):
        return smart_truncate(self.description, 30)
    
    def __unicode__(self):
        return "%s: %s (%s)" % (self.hosting_client.name, self.description, self.amount)


def create_invoice_for_hosting_clients(hostingclient_qs):
    invoice_list = []
    for hostingclient in hostingclient_qs.all():
        new_invoice = Invoice.objects.create(client=hostingclient.client, description="Website hosting")
        
        periods_invoiced = HostingInvoiceRow.objects.filter(hosting_client=hostingclient, is_hosting=True).aggregate(models.Sum('invoicerow__quantity'))['invoicerow__quantity__sum'] or 0
        periods_to_invoice = periods_invoiced + decimal.Decimal(hostingclient.billing_frequency)
        
        year = int(hostingclient.start_date.year + int(hostingclient.start_date.month + periods_to_invoice) / 12)
        month = int((hostingclient.start_date.month + periods_to_invoice) % 12)
        day = min(hostingclient.start_date.day, calendar.monthrange(year, month)[1])
        
        new_row = InvoiceRow.objects.create(
            invoice=new_invoice,
            project=Project.objects.get(slug='hosting'),
            detail='Website hosting until %s/%s/%s' % (day, month, year),
            quantity=hostingclient.billing_frequency,
            price=hostingclient.period_fee,
        )
        
        HostingInvoiceRow.objects.create(invoicerow=new_row, hosting_client=hostingclient)
        invoice_list.append(new_invoice)
    
    return invoice_list
