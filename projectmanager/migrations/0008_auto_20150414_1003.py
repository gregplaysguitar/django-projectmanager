# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0007_auto_20150413_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quoterow',
            name='quote',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='projects',
        ),
        migrations.AlterField(
            model_name='task',
            name='quoted_hours',
            field=models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.DeleteModel(
            name='QuoteRow',
        ),
    ]
