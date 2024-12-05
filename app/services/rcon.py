from types import TracebackType
from typing import Optional, Self, cast

from aiomcrcon.client import Client


class RCONClient:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.client = Client(
            host=host,
            port=port,
            password=password,
        )

    async def execute_command(self, command: str) -> str:
        response, code = await self.client.send_cmd(command)
        return cast(str, response)

    async def __aenter__(self) -> Self:
        await self.client.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.client.close()
