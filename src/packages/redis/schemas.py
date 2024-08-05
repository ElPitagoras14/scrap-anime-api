from redis_om import HashModel, Field, Migrator

from .client import redis_client


class SavedRedis(HashModel):
    anime_id: str = Field(primary_key=True, index=True)
    name: str
    image_src: str
    week_day: str

    class Meta:
        database = redis_client


Migrator().run()
