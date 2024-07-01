from redis_om import get_redis_connection

from .config import redis_settings

REDIST_HOST = redis_settings.HOST
REDIS_PORT = redis_settings.PORT


redis_client = get_redis_connection(
    host=REDIST_HOST,
    port=REDIS_PORT,
    password=None,
    decode_responses=True,
)
