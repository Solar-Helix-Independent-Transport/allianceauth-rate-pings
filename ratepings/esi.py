import logging


from django.dispatch import receiver
from django.utils import timezone
from esi.signals import esi_request_statistics

from .tasks import send_ping

logger = logging.getLogger(__name__)

@receiver(esi_request_statistics)
def esi_callback(sender, operation, status_code, headers, latency, bucket, **kwargs):

    try:
        ## Global Error Rate
        if "x-esi-error-limit-remain" in headers:
            remain = headers.get('x-esi-error-limit-remain')
            if int(remain) <=5:
                message = f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - `Global Limit` `100/60s` - remaining {remain}"
                logger.error(message)
                send_ping.delay(message)
    except Exception as e:
        logger.error(e)

    try:
        if bucket != "" and status_code > 0:
            remain = headers.get('x-ratelimit-remaining')
            total = headers.get('x-ratelimit-limit')
            group = headers.get('x-ratelimit-group')

            test = int(total.split("/")[0])*0.25

            if int(remain) <= test:
                message = f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - `{bucket}` : `{group} - {total}`- Remain: {remain}"
                logger.error(message)
                send_ping.delay(message)

    except Exception as e:
        logger.error(e)
