# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0006_auto_20150413_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttime',
            name='_time',
            field=models.DecimalField(default=0, editable=False, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='projecttime',
            old_name='_time',
            new_name='_hours',
        ),
    ]
