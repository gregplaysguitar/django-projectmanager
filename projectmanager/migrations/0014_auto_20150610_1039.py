# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def user_to_m2m(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    Organisation = apps.get_model('projectmanager', 'Organisation')
    OrganisationUser = apps.get_model('projectmanager', 'OrganisationUser')

    for org in Organisation.objects.all():
        OrganisationUser.objects.create(user=org.owner, organisation=org)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectmanager', '0013_auto_20150609_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='organisation',
            name='owner',
            field=models.ForeignKey(related_name='owned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisationuser',
            name='organisation',
            field=models.ForeignKey(to='projectmanager.Organisation'),
        ),
        migrations.AddField(
            model_name='organisationuser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisation',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='projectmanager.OrganisationUser'),
        ),
        
        migrations.RunPython(user_to_m2m),
        
        migrations.RemoveField(
            model_name='organisation',
            name='owner',
        ),
    ]
