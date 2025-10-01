# app/core/config.py
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "dev-secret"
    JWT_EXPIRES_MIN: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    APP_NAME: str = "Missing Link API"
    APP_VERSION: str = os.getenv("APP_VERSION", "0.3.0")
    GIT_COMMIT: str | None = os.getenv("GIT_COMMIT")
    BUILD_TIME: str | None = os.getenv("BUILD_TIME")


settings = Settings()
