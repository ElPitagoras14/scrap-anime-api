from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class ScraperSettings(BaseSettings):
    HOST: str
    IN_DOCKER: bool

    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename=".env", usecwd=True),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="ANIME_",
    )


scraper_settings = ScraperSettings()
