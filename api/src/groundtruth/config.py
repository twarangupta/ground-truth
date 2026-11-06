"""Typed application settings loaded from environment variables and the root .env file."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py -> groundtruth -> src -> api -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """All configuration the API reads. Field names map to env vars case-insensitively."""

    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        # .env also holds compose-only variables (POSTGRES_*), so ignore unknown keys.
        extra="ignore",
    )

    app_env: Literal["local", "test", "production"] = "local"
    database_url: PostgresDsn


@lru_cache
def get_settings() -> Settings:
    """Build Settings once and reuse it. Real environment variables override .env values."""
    return Settings()
