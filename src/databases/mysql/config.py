from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class MysqlSettings(BaseSettings):
    HOST: str
    USER: str
    PASS: str
    PORT: int
    DATABASE: str

    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename=".env", usecwd=True),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="MYSQL_",
    )


mysql_settings = MysqlSettings()
