from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from admin_restricted import RestrictedByUsers

from projectmanager.models import *


class ProjectExpenseInline(admin.TabularInline):
    model = ProjectExpense
    extra = 1
    
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

#class ProjectTimeInline(admin.TabularInline):
#   model = ProjectTime
#   extra = 1


class ProjectAdmin(RestrictedByUsers):
    user_field = 'owner'
    is_many_field = False
    
    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        return qs.annotate(latest_time=models.Max('projecttime__start'))
        
    def save_model(self, req, obj, *args, **kwargs):
        obj.owner = req.user
        return super(ProjectAdmin, self).save_model(req, obj, *args, **kwargs)

    def make_completed(self, request, queryset):
        queryset.update(completed=True)
    
    def make_hidden(self, request, queryset):
        queryset.update(hidden=True)
    
    # list_display = ('name', 'client', 'total_estimated_hours', 'total_time',
    #                 'latest_time', 'billing_type', 'total_invoiced',
    #                 'time_invoiced', 'unbilled_time', 'total_to_invoice',
    #                 'approx_hours_to_invoice', 'completed', 'links', )
    list_display = ('client', 'name', 'total_hours', 'invoiceable_hours', 
                    'invoiced_hours', 'latest_time', 'to_invoice', 'completed',
                    'links', )
    list_display_links = ('client', 'name')
    list_filter = ('completed', 'creation_date', 'billable', 'hidden', 'client')
    search_fields = ('name', 'client__name', 'slug', 'description')
    prepopulated_fields = {
        'slug': ('client', 'name',)
    }
    inlines = [ProjectExpenseInline, TaskInline, ]
    actions = ['create_invoice_for_selected', 'make_completed', 'make_hidden']
    exclude = ('owner', )
    
    def to_invoice(self, obj):
        return obj.invoiceable_hours() - obj.invoiced_hours()
    
    # def unbilled_time(self, obj):
    #     return max(0, obj.total_time() - obj.time_invoiced())
        
    def links(self, obj):
        time_url = reverse('admin:projectmanager_projecttime_changelist')
        return (u'<a href="%s?task__project__id__exact=%s">view</a> ' % 
                (time_url, obj.pk)) + \
               (u'<a href="%s">csv</a> ' % obj.projecttime_summary_url())

    def create_invoice_for_selected(self, request, queryset):
        invoice = create_invoice_for_projects(queryset)
        return HttpResponseRedirect(reverse('admin:projectmanager_invoice_change', args=(invoice.id,)))
        
    links.short_description = ' '                
    links.allow_tags = True

admin.site.register(Project, ProjectAdmin)


class ProjectTimeAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
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

# class InvoiceAdmin(RestrictedByUsers):
#     user_field = 'project__owner'
#     is_many_field = False
    
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'description', 'creation_date_display', 'subtotal', 'paid', 'invoice')
    list_filter = (# 'invoicerow__task__project',
                   'creation_date', 'paid')
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
    list_filter = ('completed', 'creation_date', )
    list_display = ('project', 'task', 'total_hours', 'invoiceable_hours',
                    'invoiced_hours', 'get_completed', )
    search_fields = ('project__name', 'task', 'comments')
    raw_id_fields = ('project',)
    
    def get_completed(self, obj):
        return obj.completion_date.date() if obj.completed else ''
    get_completed.admin_order_field = 'completed'
    get_completed.short_description = 'Completed'

admin.site.register(Task, TaskAdmin)
