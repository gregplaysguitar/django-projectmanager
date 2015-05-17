# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_clients(apps, schema_editor):
    Project = apps.get_model("projectmanager", "Project")
    Client = apps.get_model("projectmanager", "Client")
    for project in Project.objects.all():
        if project.client_old:
            client, __ = Client.objects.get_or_create(name=project.client_old)
            project.client = client
            project.save()
        

class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0004_auto_20150408_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='project',
            old_name='client',
            new_name='client_old',
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(blank=True, to='projectmanager.Client', null=True),
        ),
        migrations.RunPython(create_clients),
        migrations.RemoveField(
            model_name='project',
            name='client_old',
        ),
    ]
