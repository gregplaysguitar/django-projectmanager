# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0024_auto_20150915_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='organisation',
            name='gst_number',
            field=models.CharField(default=b'', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='payment_details',
            field=models.TextField(default=b'', help_text=b'Appears at bottom of invoice.', blank=True),
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='quantity',
            field=models.DecimalField(max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='task',
            field=models.ForeignKey(blank=True, to='projectmanager.Task', null=True),
        ),
    ]
