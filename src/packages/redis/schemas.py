from datetime import datetime
from enum import Enum
from redis_om import HashModel, Field, Migrator

from .client import redis


class DownloadType(str, Enum):
    QUEUE = "queue"
    HISTORY = "history"


class DownloadRedis(HashModel):
    id: str = Field(primary_key=True)
    date: datetime = Field(index=True)
    type: DownloadType = Field(index=True)
    file_url: str
    file_name: str
    anime: str = Field(index=True)
    episode_id: int
    description: str
    image_src: str
    progress: int
    total_size: int

    class Meta:
        database = redis


Migrator().run()
