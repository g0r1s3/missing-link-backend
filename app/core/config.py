from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "dev-secret"      # nur für DEV!
    JWT_EXPIRES_MIN: int = 30
    JWT_ALG: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
2