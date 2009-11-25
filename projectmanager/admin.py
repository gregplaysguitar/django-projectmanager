from projectmanager.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe
from admin_restricted import RestrictedByUsers
from django.core import urlresolvers


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

    def save_model(self, request, obj, form, **kwargs):
        obj.owner = request.user
        obj.save()
        """
        if not obj.users.filter(pk=obj.owner.pk).count():
            obj.users.add(obj.owner)
        print obj.users.all()
        """
    
#    list_display = ('client', 'name', 'creation_date', 'total_time', 'hourly_rate', 'total_expenses', 'total_cost', 'total_invoiced', 'total_to_invoice', 'approx_hours_to_invoice', 'completed')
    list_display = ('client', 'name', 'total_estimated_hours', 'total_time', 'total_invoiced', 'total_to_invoice', 'approx_hours_to_invoice', 'completed', 'links', )
    list_display_links = ('client', 'name')
    list_filter = ('completed', 'creation_date', 'billable')
    search_fields = ('name', 'client', 'slug', 'description', 'projectexpense__description')
    prepopulated_fields = {
        'slug': ('client', 'name',)
    }
    inlines = [ProjectExpenseInline,TaskInline,]
    actions = ['create_invoice_for_selected', ]
    exclude = ('owner', )
    
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
    links.short_description = ''                
    links.allow_tags = True


admin.site.register(Project, ProjectAdmin)


class ProjectTimeAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('project', 'description', 'start', 'end', 'total_time')
    list_filter = ('project', 'start')
    search_fields = ('description',)
    date_hierarchy = 'start'

admin.site.register(ProjectTime, ProjectTimeAdmin)


class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 2

class InvoiceAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('client', 'description', 'creation_date', 'subtotal', 'paid', 'invoice')
    list_filter = ('projects', 'creation_date', 'paid')
    inlines = [InvoiceRowInline,]
    actions = ['make_paid',]
    
    def make_paid(self, request, queryset):
        queryset.update(paid=True)

    
    def invoice(self, instance):
        return u'<a href="/invoice/%d/%s">pdf</a>' % (instance.id, instance.pdf_filename()) + u' | <a href="/invoice/%d/">html</a>' % (instance.id)
                
    invoice.allow_tags = True
    
admin.site.register(Invoice, InvoiceAdmin)



class TaskAdmin(RestrictedByUsers):
    user_field = 'project__owner'
    is_many_field = False
    
    list_display = ('project', 'task', 'completed', 'completion_date', 'creation_date')

admin.site.register(Task, TaskAdmin)

