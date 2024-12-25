import logging
from typing import Final

from mcrcon import MCRcon

from app.utils.text import remove_minecraft_colors

logger: Final[logging.Logger] = logging.getLogger(name=__name__)


class RCONClient:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.password = password

    def execute_command(self, command: str) -> str:
        with MCRcon(
            host=self.host,
            port=self.port,
            password=self.password,
        ) as rcon:
            response: str = remove_minecraft_colors(text=rcon.command(command))
            logger.info(
                ("Executed command » %s%s"),
                command,
                f"\nResponse »{response}" if response else "",
            )
            return response
