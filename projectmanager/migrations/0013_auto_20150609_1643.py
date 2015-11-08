# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def create_organisations(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    Project = apps.get_model('projectmanager', 'Project')
    Organisation = apps.get_model('projectmanager', 'Organisation')
    Invoice = apps.get_model('projectmanager', 'Invoice')
    Client = apps.get_model('projectmanager', 'Client')
    
    for proj in Project.objects.all():
        try:
            org = Organisation.objects.get(owner=proj.owner)
        except Organisation.DoesNotExist:
            org = Organisation.objects.create(name=proj.owner.first_name + ' ' + proj.owner.last_name, 
                                              owner=proj.owner)
        proj.organisation = org
        proj.save()
    
    # assume clients/invoices with no projects are bogus and can be deleted
    for inv in Invoice.objects.all():
        for row in inv.invoicerow_set.all():
            inv.organisation = row.task.project.organisation
            inv.save()
            break
        
        if not inv.organisation:
            inv.delete()
    
    for client in Client.objects.all():
        for proj in Project.objects.filter(client=client):
            client.organisation = proj.organisation
            client.save()
            break
        
        if not client.organisation:
            client.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0012_auto_20150609_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation', null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation', null=True),
        ),
        
        migrations.RunPython(create_organisations),
        
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='project',
            name='users',
        ),
        migrations.AlterField(
            model_name='client',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation'),
        ),
    ]
