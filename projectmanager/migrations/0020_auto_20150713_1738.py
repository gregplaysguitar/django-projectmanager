# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0019_auto_20150713_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='client_new',
            new_name='client',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='email',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
