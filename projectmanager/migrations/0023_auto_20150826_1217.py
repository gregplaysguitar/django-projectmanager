# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0022_set_completion_dates'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('created',)},
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='creation_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='creation_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='projectexpense',
            old_name='creation_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='projecttime',
            old_name='creation_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='creation_date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
