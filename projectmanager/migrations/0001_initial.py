# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
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
                ('hosting_client', models.ForeignKey(to='projectmanager.HostingClient')),
            ],
        ),
        migrations.CreateModel(
            name='HostingInvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_hosting', models.BooleanField(default=True)),
                ('hosting_client', models.ForeignKey(to='projectmanager.HostingClient')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, blank=True)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('address', models.TextField(blank=True)),
                ('paid', models.BooleanField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.CharField(max_length=255, blank=True)),
                ('quantity', models.DecimalField(max_digits=10, decimal_places=2)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('invoice', models.ForeignKey(to='projectmanager.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(unique=True, max_length=60)),
                ('description', models.TextField(blank=True)),
                ('completed', models.BooleanField(db_index=True)),
                ('hidden', models.BooleanField(db_index=True)),
                ('billable', models.BooleanField(default=1, db_index=True)),
                ('hourly_rate', models.DecimalField(default=80, max_digits=10, decimal_places=2)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('billing_type', models.CharField(default=b'quote', max_length=5, choices=[(b'quote', b'Quote'), (b'time', b'Time')])),
                ('owner', models.ForeignKey(related_name='project_ownership_set', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='project_membership_set', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProjectExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.TextField()),
                ('project', models.ForeignKey(to='projectmanager.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateTimeField(db_index=True)),
                ('end', models.DateTimeField(db_index=True)),
                ('description', models.TextField()),
                ('_time', models.DecimalField(null=True, editable=False, max_digits=4, decimal_places=2)),
                ('project', models.ForeignKey(to='projectmanager.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True)),
                ('description', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.CharField(max_length=255, blank=True)),
                ('quantity', models.DecimalField(max_digits=10, decimal_places=2)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quote', models.ForeignKey(to='projectmanager.Quote')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.TextField()),
                ('comments', models.TextField(blank=True)),
                ('completed', models.BooleanField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('completion_date', models.DateTimeField(null=True, editable=False)),
                ('estimated_hours', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('project', models.ForeignKey(to='projectmanager.Project')),
            ],
            options={
                'ordering': ('creation_date',),
            },
        ),
        migrations.AddField(
            model_name='invoicerow',
            name='project',
            field=models.ForeignKey(to='projectmanager.Project'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='projects',
            field=models.ManyToManyField(to='projectmanager.Project', through='projectmanager.InvoiceRow'),
        ),
        migrations.AddField(
            model_name='hostinginvoicerow',
            name='invoicerow',
            field=models.ForeignKey(to='projectmanager.InvoiceRow'),
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='invoice_rows',
            field=models.ManyToManyField(to='projectmanager.InvoiceRow', through='projectmanager.HostingInvoiceRow'),
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='owner',
            field=models.ForeignKey(related_name='hosting_client_ownership_set', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostingclient',
            name='users',
            field=models.ManyToManyField(related_name='hosting_client_membership_set', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
