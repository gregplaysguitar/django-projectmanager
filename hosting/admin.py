from django.contrib import admin
from django.core.urlresolvers import reverse

from projectmanager.admin_restricted import RestrictedByUsers

from .models import HostingClient, HostingExpense, HostingInvoiceRow


class HostingInvoiceRowInline(admin.TabularInline):
    model = HostingInvoiceRow
    extra = 0
    raw_id_fields = ('invoicerow',)


class HostingExpenseInline(admin.TabularInline):
    model = HostingExpense
    extra = 1


class HostingClientAdmin(RestrictedByUsers):
    user_field = 'owner'
    is_many_field = False
    
    list_display = ('client', 'name', 'start_date', 'total_cost', 
                    'total_invoiced', 'total_paid', 'invoice_due', )
    list_display_links = ('client', 'name')
    list_filter = ('start_date', 'invoice_due', 'termination_date', 'hidden',)
    search_fields = ('name', 'client', )
    prepopulated_fields = {
        'slug': ('client', 'name',)
    }
    inlines = [HostingInvoiceRowInline,HostingExpenseInline,]
    actions = ['create_invoice_for_selected']

    def create_invoice_for_selected(self, request, queryset):
        invoices = create_invoice_for_hosting_clients(queryset)
        if invoices:
            url = reverse('admin:projectmanager_invoice_change', 
                          args=(invoices[0].pk,))
            return HttpResponseRedirect(url + '?paid__exact=0')

admin.site.register(HostingClient, HostingClientAdmin)
