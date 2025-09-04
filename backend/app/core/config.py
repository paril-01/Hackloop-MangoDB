from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "REPLIKA"
    DATABASE_URL: str = "sqlite:///./replika.db"
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    DATA_RETENTION_DAYS: int = 30
    SESSION_TTL_SECONDS: int = 3600
    SESSION_CLEANUP_INTERVAL_SECONDS: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
