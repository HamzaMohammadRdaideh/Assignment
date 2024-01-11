# core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str = 'mongodb://localhost:27017'
    MONGO_DB_NAME: str = "user"


settings = Settings()
