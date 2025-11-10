import json

import logging

import requests
from celery import shared_task

from . import app_settings

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=None)
def send_ping(self, message):
    url = app_settings.RP_WEBHOOK
    if url:
        payload = {
            "content": message
        }

        custom_headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url,
                                headers=custom_headers,
                                json=payload,
                                params={'wait': True})

        if response.status_code in [200, 204]:
            logger.debug(f"`{message}` Sent!")
        elif response.status_code == 429:
            errors = json.loads(response.content.decode('utf-8'))
            wh_sleep = (int(errors['retry_after']) / 1000) + 0.15
            logger.warning(
                f"Webhook rate limited: trying again in {wh_sleep} seconds...")
            self.retry(countdown=wh_sleep)
        else:
            response.raise_for_status()
        # TODO 404/403/500 etc etc etc etc
