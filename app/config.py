import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./use_cases.db")
    app_name: str = os.getenv("APP_NAME", "AI Use Case Explorer")


settings = Settings()
