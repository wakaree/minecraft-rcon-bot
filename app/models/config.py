from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.const import ENV_FILE
from app.utils.custom_types import IntList


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    drop_pending_updates: bool
    admins: IntList


class RconConfig(EnvSettings, env_prefix="RCON_"):
    host: str
    port: int
    password: SecretStr


class WhiteListConfig(EnvSettings, env_prefix="WHITELIST_"):
    add_command: str
    remove_command: str


class AppConfig(EnvSettings):
    telegram: TelegramConfig
    rcon: RconConfig
    whitelist: WhiteListConfig
