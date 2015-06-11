# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0016_auto_20150611_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='comments',
        ),
    ]
