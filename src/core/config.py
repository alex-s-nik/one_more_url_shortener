import os
from logging import config as logging_config

from pydantic import BaseSettings, Field, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLACKLIST = (
    '127.0.0.2',
)

SHORTEN_URL_LEN = 6


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: PostgresDsn
    engine_echo: bool = Field(True, env='ENGINE_ECHO')
    project_name: str = Field('url_shortener', env='PROJECT_NAME')
    project_host: str = Field('0.0.0.0', env='PROJECT_HOST')
    project_port: int = Field(8000, env='PROJECT_PORT')
    secret: str = 'SECRET_WORD'

    class Config:
        env_file = '.env'


app_settings = AppSettings()
