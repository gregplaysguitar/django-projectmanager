# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


CLIENT_FIELDS = ('owner', 'client', 'name', 'slug', 'billing_frequency', 
                 'billing_period', 'period_fee', 'start_date', 
                 'invoice_due', 'termination_date', 'hidden', )
ROW_FIELDS = ('invoicerow', 'is_hosting', )
EXPENSE_FIELDS = ('creation_date', 'amount', 'description', 'writeoff')


def import_hosting(apps, schema_editor):
    HostingClient = apps.get_model("hosting", "HostingClient")
    HostingInvoiceRow = apps.get_model("hosting", "HostingInvoiceRow")
    HostingExpense = apps.get_model("hosting", "HostingExpense")

    HostingClient_old = apps.get_model("projectmanager", "HostingClient")
    HostingInvoiceRow_old = apps.get_model("projectmanager", 
                                           "HostingInvoiceRow")
    HostingExpense_old = apps.get_model("projectmanager", "HostingExpense")


    for old_h in HostingClient_old.objects.all():
        params = dict((f, getattr(old_h, f)) for f in CLIENT_FIELDS)
        h = HostingClient.objects.create(**params)
        
        for u in old_h.users.all():
            h.users.add(u)
        
        for old_r in HostingInvoiceRow_old.objects.filter(hosting_client=old_h):
            params = dict((f, getattr(old_r, f)) for f in ROW_FIELDS)
            HostingInvoiceRow.objects.create(hosting_client=h, **params)
        
        for old_e in HostingExpense_old.objects.filter(hosting_client=old_h):
            params = dict((f, getattr(old_e, f)) for f in EXPENSE_FIELDS)
            HostingExpense.objects.create(hosting_client=h, **params)
            

class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0001_initial'),
        ('projectmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_hosting),
    ]
