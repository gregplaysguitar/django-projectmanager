# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_clients(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return
  
    Invoice = apps.get_model('projectmanager', 'Invoice')
    Client = apps.get_model('projectmanager', 'Client')
    for obj in Invoice.objects.all():
        client_kwargs = {'name': obj.client, 
                         'organisation': obj.organisation}
        try:
            client = Client.objects.get(**client_kwargs)
        except Client.DoesNotExist:
            client = Client.objects.create(**client_kwargs)
        
        if not client.email:
            client.email = obj.email
        client.invoice_detail = obj.address

        client.save()
        obj.client_new = client
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0018_auto_20150713_1737'),
    ]

    operations = [
        migrations.RunPython(create_clients),
    ]
