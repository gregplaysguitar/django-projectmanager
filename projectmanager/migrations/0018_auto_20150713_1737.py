# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0017_remove_task_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='invoice_detail',
            field=models.TextField(default=b'', help_text='E.g. client address', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='client_new',
            field=models.ForeignKey(blank=True, to='projectmanager.Client', null=True),
        ),
    ]
