import os

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_ENGINE: str = 'django.db.backends.postgresql'
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


database_settings = DatabaseSettings(
    DB_NAME=os.environ.get('DB_NAME'),
    DB_USER=os.environ.get('DB_USER'),
    DB_PASSWORD=os.environ.get('DB_PASSWORD'),
    DB_HOST=os.environ.get('DB_HOST'),
    DB_PORT=os.environ.get('DB_PORT', 5432),
)
