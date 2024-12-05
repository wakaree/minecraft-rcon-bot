from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(message: Message) -> Any:
    return message.answer("Hello, {name}!".format(name=message.from_user.mention_html()))
