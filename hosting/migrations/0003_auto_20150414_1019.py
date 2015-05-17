# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0002_import'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostingclient',
            name='invoice_rows',
            field=models.ManyToManyField(to='projectmanager.InvoiceRow', through='hosting.HostingInvoiceRow'),
        ),
        migrations.AlterField(
            model_name='hostingclient',
            name='owner',
            field=models.ForeignKey(related_name='hosting_client_ownership_set', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hostingclient',
            name='users',
            field=models.ManyToManyField(related_name='hosting_client_membership_set', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='hostinginvoicerow',
            name='invoicerow',
            field=models.ForeignKey(to='projectmanager.InvoiceRow'),
        ),
    ]
