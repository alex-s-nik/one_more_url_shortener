import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'url_shortener')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLACKLIST = (
    '127.0.0.2',
)

SHORTEN_URL_LEN = 6


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: PostgresDsn
    secret: str = 'SECRET_WORD'

    class Config:
        env_file = '.env'


app_settings = AppSettings()
