# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
                ('quote', models.ForeignKey(to='quotes.Quote')),
            ],
        ),
    ]
