import logging
import redis
from django.apps import AppConfig
from django.conf import settings

from prometheus_redis_client import REGISTRY

logger = logging.getLogger(__name__)

# Load all the prom models
import ratepings

class AllianceAuthRatePingsConfig(AppConfig):
    name = ratepings.__name__
    verbose_name = f"Auth Rate Pings {ratepings.__version__}"

    def ready(self):        
        # load the esi signal client.
        try:
            import ratepings.esi
        except Exception as e:
            logger.error(e)

