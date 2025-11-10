from django.conf import settings

RP_WEBHOOK = getattr(settings, 'RP_WEBHOOK', False)
