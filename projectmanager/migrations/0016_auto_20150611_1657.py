# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0015_projecttime_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='billing_type',
        ),
        migrations.RemoveField(
            model_name='project',
            name='slug',
        ),
    ]
