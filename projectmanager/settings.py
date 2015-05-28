from django.conf import settings


SALES_TAX = getattr(settings, 'PROJECTMANAGER_SALES_TAX', 0.15)
HOURLY_RATE = getattr(settings, 'PROJECTMANAGER_HOURLY_RATE', 80)
