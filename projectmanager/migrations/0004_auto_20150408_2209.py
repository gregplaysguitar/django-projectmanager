# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0003_projecttime_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttime',
            name='project',
        ),
        migrations.AlterField(
            model_name='task',
            name='comments',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
