# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_hours(apps, schema_editor):
    Task = apps.get_model("projectmanager", "Task")
    Task.objects.filter(estimated_hours__isnull=True).update(estimated_hours=0)
class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_hours),
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='estimated_hours',
            field=models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2),
        ),
    ]
