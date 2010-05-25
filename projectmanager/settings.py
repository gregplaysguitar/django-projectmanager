from django.conf import settings



BILLING_PERIOD_MONTHS_CHOICES = getattr(settings, 'PROJECTMANAGER_BILLING_PERIOD_MONTH_CHOICES', (
    ('6', '6 monthly',),
    ('12', 'Yearly'),
))

BILLING_PERIOD_MONTHS_DEFAULT = getattr(settings, 'PROJECTMANAGER_BILLING_PERIOD_MONTH_DEFAULT', '12')
