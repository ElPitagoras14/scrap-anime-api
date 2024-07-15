from datetime import datetime
from redis_om import HashModel, Field, Migrator

from .client import redis_client


class DownloadRedis(HashModel):
    id: str = Field(primary_key=True)
    date: datetime = Field(index=True)
    file_url: str
    file_name: str
    anime: str = Field(index=True)
    episode_id: int
    title: str
    image_src: str
    progress: int
    total_size: int

    class Meta:
        database = redis_client


class SavedRedis(HashModel):
    anime_id: str = Field(primary_key=True, index=True)
    name: str
    image_src: str
    week_day: str

    class Meta:
        database = redis_client


Migrator().run()
