from django.conf.urls.defaults import *

urlpatterns = patterns('projectmanager.views',
    (r'^calendar/$', 'project_time_calendar'),
    (r'^api/time/list/', 'api_project_time_list'),
    (r'^api/time/add/', 'api_project_time_add'),
    (r'^api/time/edit/', 'api_project_time_edit'),
    (r'^api/time/move/', 'api_project_time_move'),

    (r'^tasks/$', 'tasks'),
    (r'^tasks/(\d+)/$', 'tasks'),
    (r'^tasks/(all)/$', 'tasks'),

    (r'^invoice/(\d+)/$', 'invoice'),
    (r'^invoice/(\d+)/.+\.(pdf)$', 'invoice'),

    (r'^itemise/(\d+)/$', 'projecttime_summary'),

    (r'^create_invoice_for_project/(\d+)/$', 'create_invoice_for_project'),

)

