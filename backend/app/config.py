"""
Application Configuration for Marketing Mix Copilot
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AI Marketing Mix & Incrementality Copilot"
    version: str = "1.0.0"
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./copilot.db")
    environment: str = os.getenv("ENVIRONMENT", "development")
    cors_origins: list = ["*"]


settings = Settings()
