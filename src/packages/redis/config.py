from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class RedisSettings(BaseSettings):
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename=".env", usecwd=True),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
    )


redis_settings = RedisSettings()
