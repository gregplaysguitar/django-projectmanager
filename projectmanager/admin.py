from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.core import urlresolvers

from admin_restricted import RestrictedByUsers

from projectmanager.models import *


class ProjectExpenseInline(admin.TabularInline):
    model = ProjectExpense
    extra = 1
    
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    raw_id_fields = ('invoicerow',)

#class ProjectTimeInline(admin.TabularInline):
#   model = ProjectTime
#   extra = 1
#   raw_id_fields = ('invoicerow',)




class ProjectAdmin(RestrictedByUsers):
    user_field = 'owner'
    is_many_field = False
    
    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        return qs.annotate(latest_time=models.Max('projecttime__start'))
        
    def save_model(self, request, obj, *args, **kwargs):
        obj.owner = request.user
        super(ProjectAdmin, self).save_model(request, obj, *args, **kwargs)

    def make_completed(self, request, queryset):
        queryset.update(completed=True)
    
    def make_hidden(self, request, queryset):
        queryset.update(hidden=True)
    
    list_display = ('name', 'client', 'total_estimated_hours', 'total_time', 'time_invoiced', 'billable_task_time', 'billable_non_task_time', 'latest_time', 'links', )
    list_display_links = ('client', 'name')
    list_filter = ('completed', 'creation_date', 'billable', 'hidden', 'client', 'billing_type')
    search_fields = ('name', 'client', 'slug', 'description')
    prepopulated_fields = {
        'slug': ('client', 'name',)
    }
    inlines = [ProjectExpenseInline,TaskInline,]
    actions = ['create_invoice_for_selected', 'make_completed', 'make_hidden']
    exclude = ('owner', )
    
    def unbilled_time(self, obj):
        return max(0, obj.total_time() - obj.time_invoiced())
    
    def latest_time(self, obj):
        try:
            return obj.projecttime_set.all().order_by('-start')[0].start.date()
        except IndexError:
            return None
    latest_time.admin_order_field = 'latest_time'
        
    def create_invoice(self, instance):
        return u'<a href="/create_invoice_for_project/%d/">create</a>' % (instance.id)

    def links(self, instance):
        return (u'<a href="%s?project__id__exact=%s">view</a> ' % (urlresolvers.reverse('admin:projectmanager_projecttime_changelist'), instance.pk)) + \
               (u'<a href="%s">csv</a> ' % instance.projecttime_summary_url())


    def create_invoice_for_selected(self, request, queryset):
        invoice = create_invoice_for_projects(queryset)
        return HttpResponseRedirect(urlresolvers.reverse('admin:projectmanager_invoice_change', args=(invoice.id,)))
        
    create_invoice.short_description = 'Invoice'                
    create_invoice.allow_tags = True
    links.short_description = ' '                
    links.allow_tags = True


admin.site.register(Project, ProjectAdmin)


class ProjectTimeAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('project', 'task', 'description', 'start', 'end', 'total_time')
    list_filter = ('project', 'start')
    search_fields = ('description',)
    date_hierarchy = 'start'
    raw_id_fields = ('project', 'task', 'invoicerow')

admin.site.register(ProjectTime, ProjectTimeAdmin)


class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 2
    raw_id_fields = ('project', )
    exclude = ('tasks', 'time')

class InvoiceAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('client', 'description', 'creation_date_display', 'subtotal', 'paid', 'invoice')
    list_filter = ('projects', 'creation_date', 'paid')
    inlines = [InvoiceRowInline,]
    actions = ['make_paid',]
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

    def creation_date_display(self, instance):
        return datetime.date(instance.creation_date.year, instance.creation_date.month, instance.creation_date.day)
    creation_date_display.admin_order_field = 'creation_date'
    
    def invoice(self, instance):
        return u'<a href="/invoice/%d/%s">pdf</a>' % (instance.id, instance.pdf_filename()) + u' | <a href="/invoice/%d/">html</a>' % (instance.id)
                
    invoice.allow_tags = True
    
admin.site.register(Invoice, InvoiceAdmin)



class TaskAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    list_filter = ('completed', 'creation_date', 'project', )
    list_display = ('project', 'task', 'estimated_hours', 'completed', 'completion_date', 'creation_date')
    search_fields = ('project__name', 'task', 'comments')
    raw_id_fields = ('project', 'invoicerow')
admin.site.register(Task, TaskAdmin)


class HostingInvoiceRowInline(admin.TabularInline):
    model = HostingInvoiceRow
    extra = 0
    raw_id_fields = ('invoicerow',)
   

class HostingExpenseInline(admin.TabularInline):
    model = HostingExpense
    extra = 1
    
    
class HostingClientAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('client', 'name', 'start_date', 'total_cost', 'total_invoiced', 'total_paid', 'invoice_due', )
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
            return HttpResponseRedirect(urlresolvers.reverse('admin:projectmanager_invoice_change', args=(invoices[0].pk,)) + '?paid__exact=0')
        
    

admin.site.register(HostingClient, HostingClientAdmin)


admin.site.register(InvoiceRow, 
    search_fields = ('invoice__client', 'detail'),
    list_display = ('project', 'invoice', 'amount', 'detail', 'invoice_date'),
    list_filter = ('project', 'invoice', ),
)





class QuoteRowInline(admin.TabularInline):
    model = QuoteRow
    extra = 1
    
    
class QuoteAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False

    list_display = ('client', 'description', 'creation_date', 'quote', )
    list_filter = ('creation_date',)
    search_fields = ('description', 'client', )
    inlines = [QuoteRowInline, ]
    
    def quote(self, instance):
        return u'<a href="/quote/%d/%s">pdf</a>' % (instance.id, instance.pdf_filename()) + u' | <a href="/quote/%d/">html</a>' % (instance.id)
    quote.allow_tags = True
    
       
admin.site.register(Quote, QuoteAdmin)
