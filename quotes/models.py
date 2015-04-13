# import datetime, decimal
# import hashlib

from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.db.models import Q, Sum


class Quote(models.Model):
    client = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    description = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    notes = models.TextField(blank=True, default='')

    def pdf_filename(self):
        return "Quote %s - %s - %s.pdf" % (self.creation_date.strftime("%Y-%m-%d"), self.client, self.description)
    
    def subtotal(self):
        return sum(float(row.amount()) for row in self.quoterow_set.all())
    
    def gst_amount(self):
        return (float(self.subtotal()) * .15)
    
    def total(self):
        return (float(self.subtotal()) * 1.15)
    
    @models.permalink
    def get_absolute_url(self):
        return ('projectmanager.views.quote', [self.pk])


class QuoteRow(models.Model):
    quote = models.ForeignKey(Quote)
    detail = models.CharField(max_length=255, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def amount(self):
        return (self.price * self.quantity)
