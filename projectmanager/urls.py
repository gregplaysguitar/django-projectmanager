from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^calendar/$', views.project_time_calendar),
    url(r'^api/time/list/', views.api_project_time_list),
    url(r'^api/time/add/', views.api_project_time_add),
    url(r'^api/time/edit/', views.api_project_time_edit),
    url(r'^api/time/move/', views.api_project_time_move),

    url(r'^tasks/$', views.tasks),
    url(r'^tasks/(\d+)/$', views.tasks),
    url(r'^tasks/(all)/$', views.tasks),

    url(r'^invoice/(\d+)/$', views.invoice),
    url(r'^invoice/(\d+)/.+\.(pdf)$', views.invoice),

    url(r'^quote/(\d+)/$', views.quote),
    url(r'^quote/(\d+)/.+\.(pdf)$', views.quote),

    url(r'^itemise/(\d+)/$', views.projecttime_summary),

    url(r'^create_invoice_for_project/(\d+)/$', views.create_invoice_for_project),

]
