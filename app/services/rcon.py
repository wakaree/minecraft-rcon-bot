from typing import cast

from mcrcon import MCRcon


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
            return cast(str, rcon.command(command))
