# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def projecttime_users(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    ProjectTime = apps.get_model('projectmanager', 'ProjectTime')

    for ptime in ProjectTime.objects.all():
        ptime.user = ptime.task.project.organisation.users.all()[0]
        ptime.save()
        
        
class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectmanager', '0014_auto_20150610_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttime',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        
        migrations.RunPython(projecttime_users),
        
        migrations.AlterField(
            model_name='projecttime',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
