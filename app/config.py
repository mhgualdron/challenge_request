from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database Configuration
    DB_SERVER: str = "localhost"
    DB_USER: str = "sa"
    DB_PASSWORD: str = "Challenge123!"
    DB_NAME: str = "challenge_db"

    # Security
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App Settings
    APP_ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def sqlalchemy_url(self) -> str:
        return f"mssql+pymssql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"

settings = Settings()
