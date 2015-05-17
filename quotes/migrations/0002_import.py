# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


QUOTE_FIELDS = ('client', 'address', 'description', 'creation_date', 'notes', )
QUOTEROW_FIELDS = ('detail', 'quantity', 'price', )


def import_quotes(apps, schema_editor):
    Quote = apps.get_model("quotes", "Quote")
    QuoteRow = apps.get_model("quotes", "QuoteRow")
    Quote_old = apps.get_model("projectmanager", "Quote")
    QuoteRow_old = apps.get_model("projectmanager", "QuoteRow")


    for old_q in Quote_old.objects.all():
        params = dict((f, getattr(old_q, f)) for f in QUOTE_FIELDS)
        q = Quote.objects.create(**params)
        for old_qr in QuoteRow_old.objects.filter(quote=old_q):
            params = dict((f, getattr(old_qr, f)) for f in QUOTEROW_FIELDS)
            QuoteRow.objects.create(quote=q, **params)


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
        ('projectmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_quotes),
    ]
