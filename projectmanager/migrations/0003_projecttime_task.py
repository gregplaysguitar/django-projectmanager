# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_project_tasks(apps, schema_editor):
    Project = apps.get_model("projectmanager", "Project")
    ProjectTime = apps.get_model("projectmanager", "ProjectTime")
    InvoiceRow = apps.get_model("projectmanager", "InvoiceRow")
    Task = apps.get_model("projectmanager", "Task")
    for project in Project.objects.all():
        site_task = Task.objects.create(project=project, task=project.name,
                                        completed=True)
        project.projecttime_set.update(task=site_task)
        InvoiceRow.objects.filter(project=project).update(task=site_task)


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0002_modernise_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttime',
            name='task',
            field=models.ForeignKey(to='projectmanager.Task', null=True),
        ),
        migrations.AddField(
            model_name='invoicerow',
            name='task',
            field=models.ForeignKey(to='projectmanager.Task', null=True),
        ),
        migrations.RunPython(create_project_tasks),
        migrations.AlterField(
            model_name='projecttime',
            name='task',
            field=models.ForeignKey(to='projectmanager.Task'),
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='task',
            field=models.ForeignKey(to='projectmanager.Task'),
        ),
    ]
