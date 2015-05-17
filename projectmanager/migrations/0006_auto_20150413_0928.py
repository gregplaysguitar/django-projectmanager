# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0005_auto_20150410_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='estimated_hours',
            new_name='quoted_hours',
        ),
        migrations.AlterField(
            model_name='projecttime',
            name='description',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
