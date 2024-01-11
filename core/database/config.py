from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "user"

    class Config:
        env_file = ".env"


database_settings = DatabaseSettings()
