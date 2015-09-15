# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0023_auto_20150826_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='task',
            field=models.ForeignKey(to='projectmanager.Task', null=True),
        ),
    ]
