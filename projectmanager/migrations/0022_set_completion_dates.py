# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models, migrations
from django.conf import settings


def set_completion_date(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    Task = apps.get_model('projectmanager', 'Task')
    for obj in Task.objects.all():
        if obj.completed and not obj.completion_date:
            obj.completion_date = datetime.now()
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0021_auto_20150727_1051'),
    ]

    operations = [
        migrations.RunPython(set_completion_date),
    ]
