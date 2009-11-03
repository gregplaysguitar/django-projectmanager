from django.conf.urls.defaults import *
from django.conf import settings
#import os, re

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

    
urlpatterns = patterns('',

    (r'', include('projectmanager.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
    
    

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    (r'', include(admin.site.urls)),

)

