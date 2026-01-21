from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseModel):
    token: str = Field(..., description="Telegram bot token")


class AppSettings(BaseModel):
    downloads_dir: Path = Field(default_factory=lambda: Path("./downloads"))
    temp_dir: Path = Field(default_factory=lambda: Path("./tmp"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_prefix="SAVER_")

    bot: BotSettings
    app: AppSettings = AppSettings()


@dataclass(slots=True)
class SettingsLoader:
    config_path: Path = Path("config.toml")

    def load(self) -> Settings:
        if self.config_path.exists():
            data = tomllib.loads(self.config_path.read_text(encoding="utf-8"))
            return Settings.model_validate(data)
        return Settings()
