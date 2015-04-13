# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0008_auto_20150414_1003'),
        
        # make sure data migrated before removing tables
        ('hosting', '0002_import'), 
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostingclient',
            name='invoice_rows',
        ),
        migrations.RemoveField(
            model_name='hostingclient',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='hostingclient',
            name='users',
        ),
        migrations.RemoveField(
            model_name='hostingexpense',
            name='hosting_client',
        ),
        migrations.RemoveField(
            model_name='hostinginvoicerow',
            name='hosting_client',
        ),
        migrations.RemoveField(
            model_name='hostinginvoicerow',
            name='invoicerow',
        ),
        migrations.DeleteModel(
            name='HostingClient',
        ),
        migrations.DeleteModel(
            name='HostingExpense',
        ),
        migrations.DeleteModel(
            name='HostingInvoiceRow',
        ),
    ]
