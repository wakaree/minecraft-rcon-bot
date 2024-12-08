from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message, User

from app.controllers.user import update_nickname
from app.services.database import Database
from app.telegram.helpers.text import answer_usage

router: Final[Router] = Router(name=__name__)
router.message.filter(Command("nickname"))


@router.message(MagicData(F.command.args.as_("nickname")), F.reply_to_message)
async def set_nickname(
    message: Message,
    nickname: str,
    database: Database,
) -> Any:
    aiogram_user: User = message.reply_to_message.from_user
    old_nickname, nickname = update_nickname(
        user_id=aiogram_user.id,
        username=aiogram_user.username,
        nickname=nickname,
        database=database,
    )
    return message.answer(
        text="<b>👤 Nickname »</b> <code>{old}</code> → <code>{new}</code>".format(
            old=old_nickname,
            new=nickname,
        )
    )


@router.message()
async def answer_nickname_usage(message: Message) -> Any:
    return answer_usage(
        message=message,
        command="nickname [new_nickname]",
        must_reply=True,
    )
