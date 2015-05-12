# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0010_client_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoicerow',
            options={'ordering': ('task__project__name', 'task__task')},
        ),
    ]
