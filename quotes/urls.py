from django.conf.urls import *

from . import views

urlpatterns = [
    
    url(r'^quote/(\d+)/.+\.html$', views.quote),
    url(r'^quote/(\d+)/.+\.(pdf)$', views.quote),

]
