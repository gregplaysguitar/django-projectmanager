from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^calendar/$', views.project_time_calendar),
    url(r'^calendar/_api/tasks.json$', views.project_task_data),
    url(r'^calendar/_api/time/list/', views.api_project_time_list),
    url(r'^calendar/_api/time/add/', views.api_project_time_add),
    url(r'^calendar/_api/time/edit/', views.api_project_time_edit),
    url(r'^calendar/_api/time/move/', views.api_project_time_move),

    url(r'^tasks_old/$', views.tasks),
    url(r'^tasks_old/(\d+)/$', views.tasks),
    url(r'^tasks_old/(all)/$', views.tasks),

    url(r'^invoice/(\d+)/$', views.invoice),
    url(r'^invoice/(\d+)/.+\.(pdf)$', views.invoice),

    url(r'^itemise/(\d+)/$', views.projecttime_summary),

    url(r'^create_invoice_for_project/(\d+)/$', views.create_invoice_for_project),
        
]
