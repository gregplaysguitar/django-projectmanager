# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_archived(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    Project = apps.get_model('projectmanager', 'Project')
    for obj in Project.objects.all():
        obj.archived = obj.archived or obj.hidden
        obj.save()
        

class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0011_auto_20150512_1221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='completed',
            new_name='archived',
        ),
        migrations.RemoveField(
            model_name='project',
            name='billable',
        ),
        migrations.RunPython(set_archived),
        migrations.RemoveField(
            model_name='project',
            name='hidden',
        ),
    ]
