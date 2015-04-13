# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0008_auto_20150414_1003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HostingClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(unique=True, max_length=60)),
                ('billing_frequency', models.CharField(default=b'12', verbose_name='billing type', max_length=10, editable=False, choices=[(b'6', b'6 monthly'), (b'12', b'Yearly')])),
                ('billing_period', models.CharField(default=b'month', max_length=10, editable=False)),
                ('period_fee', models.DecimalField(default=25, max_digits=10, decimal_places=2)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('invoice_due', models.BooleanField(editable=False, db_column=b'invoice_due')),
                ('termination_date', models.DateField(null=True, blank=True)),
                ('hidden', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='HostingExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.TextField()),
                ('writeoff', models.BooleanField(default=False)),
                ('hosting_client', models.ForeignKey(to='hosting.HostingClient')),
            ],
        ),
        migrations.CreateModel(
            name='HostingInvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_hosting', models.BooleanField(default=True)),
                ('hosting_client', models.ForeignKey(to='hosting.HostingClient')),
                ('invoicerow', models.ForeignKey(related_name='related_2', to='projectmanager.InvoiceRow')),
            ],
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='invoice_rows',
            field=models.ManyToManyField(related_name='related_1', through='hosting.HostingInvoiceRow', to='projectmanager.InvoiceRow'),
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='owner',
            field=models.ForeignKey(related_name='hosting_client_ownership_set2', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='users',
            field=models.ManyToManyField(related_name='hosting_client_membership_set2', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
