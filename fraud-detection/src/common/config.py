from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.paths import CONFIGS_DIR


class Settings(BaseSettings):
    app_name: str = Field(default="FinShield Fraud Detection Platform")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")
    random_state: int = Field(default=42)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


def load_yaml_config(filename: str) -> dict[str, Any]:
    config_path = Path(CONFIGS_DIR) / filename
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}. "
            f"Resolved CONFIGS_DIR={CONFIGS_DIR}"
        )

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_base_config() -> dict[str, Any]:
    return load_yaml_config("base.yaml")