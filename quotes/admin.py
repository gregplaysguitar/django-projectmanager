from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse

from projectmanager.admin_restricted import RestrictedByUsers

from .models import Quote, QuoteRow


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
        url = reverse('quotes.views.quote', args=(instance.pk, ))
        pdf_url = reverse('quotes.views.quote', 
                          args=(instance.pk, instance.pdf_filename()))
        return u'<a href="%s">pdf</a>' % pdf_url + \
               u' | <a href="%s">html</a>' % url
    quote.allow_tags = True

admin.site.register(Quote, QuoteAdmin)
