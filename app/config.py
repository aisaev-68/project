import os
import pathlib
import typing
from dotenv import load_dotenv
from pathlib import Path
# from pydantic import BaseSettings
from pydantic import Extra, Field, model_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Dict, Optional, Union

from pydantic import PostgresDsn, validator, field_validator
from functools import lru_cache
from sqlalchemy.engine.url import URL

load_dotenv()


class Settings(BaseSettings):
    """
    Класс настроек.
    """
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding='utf-8')
    DEBUG: bool = Field(default=False)
    DB_USER: str = Field(default="admin")
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    DB_NAME: str = Field(default="postgres")
    DB_HOST: str = Field(default="postgres")
    DB_PORT: int = Field(default=5432)
    FOLDER_LOG: Path = Field(default="logs/")
    INDICATOR_PLAN: str = Field(default='план')
    INDICATOR_FACT: str = Field(default='факт')
    POSTGRES_ECHO: bool = Field(default=False)
    DB_URI: str | None = Field(default=None)

    @classmethod
    def get_path(cls, path: Path) -> Path:
        file_path = Path(__file__).parent / path
        file_path.mkdir(exist_ok=True, parents=True)
        abs_path = file_path.absolute()
        return abs_path

    @model_validator(mode='after')
    def change_path(self):
        """
        Метод класса для корректировки путей.
        :return:
        """
        self.DB_URI = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        self.FOLDER_LOG = self.get_path(self.FOLDER_LOG)

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()

