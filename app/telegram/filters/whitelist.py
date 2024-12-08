from typing import Any

from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import Message


class WhitelistCommandFilter(Command):
    def __init__(self) -> None:
        super().__init__("whitelist", magic=F.args.split(maxsplit=1).as_("args"))

    async def __call__(self, message: Message, bot: Bot) -> bool | dict[str, Any]:
        if message.reply_to_message is None:
            return False
        result: bool | dict[str, Any] = await super().__call__(message, bot)
        if not isinstance(result, dict):
            return False
        action, *nickname = result["args"]
        return {"action": action, "nickname": nickname[0] if nickname else None}
