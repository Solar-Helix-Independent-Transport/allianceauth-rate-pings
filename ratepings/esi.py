import logging
import json

from django.dispatch import receiver
from esi.signals import esi_request_statistics

logger = logging.getLogger(__name__)

@receiver(esi_request_statistics)
def esi_callback(sender, operation, status_code, headers, latency, bucket, **kwargs):
   
    try:
        ## Global Error Rate
        if "x-esi-error-limit-remain" in headers:
            remain = headers.get('x-esi-error-limit-remain')
            if int(remain) <=5:
                logger.error(
                    f"Global Limit - remain {remain}"
                )

    except Exception as e:
        logger.error(e)

    try:
        if bucket != "" and status_code > 0:
            remain = headers.get('x-ratelimit-remaining')
            total = headers.get('x-ratelimit-limit')
            group = headers.get('x-ratelimit-group')

            if int(remain) <=5:
                logger.error(
                    f"`{bucket}` : `{group} - {total}`- Remain: {remain}"
                )

    except Exception as e:
        logger.error(e)
