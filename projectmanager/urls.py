from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^calendar/$', views.calendar, {},
        'projectmanager_calendar'),
    url(r'^calendar/_api/tasks.json$', views.project_task_data, {},
        'projectmanager_project_task_data'),
    url(r'^calendar/_api/time/list/$', views.api_project_time_list, {},
        'projectmanager_api_project_time_list'),
    url(r'^calendar/_api/projecttime/$', views.api_projecttime, {},
        'projectmanager_api_projecttime'),
    url(r'^calendar/_api/projecttime/(\d+)$', views.api_projecttime, {},
        'projectmanager_api_projecttime'),


    # Deprecated
    # url(r'^calendar/_api/time/add/$', views.api_project_time_add),
    # url(r'^calendar/_api/time/edit/$', views.api_project_time_edit),
    # url(r'^calendar/_api/time/move/$', views.api_project_time_move),
    #
    #
    # url(r'^tasks_old/$', views.tasks),
    # url(r'^tasks_old/(\d+)/$', views.tasks),
    # url(r'^tasks_old/(all)/$', views.tasks),

    # TODO reinstate
    # url(r'^invoice/(\d+)/$', views.invoice, {},
    #     'projectmanager_invoice'),
    # url(r'^invoice/(\d+)/.+\.(pdf)$', views.invoice, {},
    #     'projectmanager_invoice'),

    # url(r'^itemise/(\d+)/$', views.projecttime_summary, {},
    #     'projectmanager_projecttime_summary'),

]
