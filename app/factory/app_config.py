from __future__ import annotations

from app.models.config import AppConfig, RconConfig, TelegramConfig, WhiteListConfig


# noinspection PyArgumentList
def create_app_config() -> AppConfig:
    return AppConfig(
        telegram=TelegramConfig(),
        rcon=RconConfig(),
        whitelist=WhiteListConfig(),
    )
