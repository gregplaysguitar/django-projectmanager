from django.conf.urls.defaults import *

urlpatterns = patterns('projectmanager.views',

#    (r'^project/[0-9A-z_\-]+/$', 'view_project'),
    (r'^time/(\d{4}-\d{2}-\d{2})/(\d{1,2})-(\d{1,2})/$', 'project_time'),
    (r'^time/(\d{4}-\d{2}-\d{2})/$', 'project_time'),
    (r'^time/$', 'project_time'),
#    (r'^tasks(?:\/|$)', 'tasks'),
    (r'^tasks/$', 'tasks'),
    (r'^tasks/(\d+)/$', 'tasks'),
    
    (r'^invoice/(\d+)/$', 'invoice'),
    (r'^invoice/(\d+)/.+\.(pdf)$', 'invoice'),
    
    (r'^create_invoice_for_project/(\d+)/$', 'create_invoice_for_project'),

)

