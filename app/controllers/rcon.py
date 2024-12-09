from app.models.config import AppConfig
from app.services.rcon import RCONClient


def add_to_whitelist(nickname: str, rcon: RCONClient, config: AppConfig) -> None:
    rcon.execute_command(command=config.whitelist.add_command.format(nickname))


def remove_from_whitelist(nickname: str, rcon: RCONClient, config: AppConfig) -> None:
    rcon.execute_command(command=config.whitelist.remove_command.format(nickname))
