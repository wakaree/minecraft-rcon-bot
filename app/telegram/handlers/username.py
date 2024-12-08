from typing import Any, Final, Optional

from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message, User

from app.models.dto.user import UserDto
from app.services.database import Database

router: Final[Router] = Router(name=__name__)
router.message.filter(Command("nickname"))


@router.message(MagicData(F.command.args.as_("nickname")), F.reply_to_message)
async def set_username(
    message: Message,
    nickname: str,
    database: Database,
) -> Any:
    aiogram_user: User = message.reply_to_message.from_user
    user: Optional[UserDto] = database.get_user(user_id=aiogram_user.id)
    if user is None:
        user = UserDto(id=aiogram_user.id, username=aiogram_user.username)
    old_nickname: Optional[str] = user.nickname
    user.nickname = nickname
    database.set_user(user)
    return message.answer(
        text="<b>👤 Nickname »</b> <code>{old}</code> → <code>{new}</code>".format(
            old=old_nickname,
            new=nickname,
        )
    )


@router.message()
async def answer_usage(message: Message) -> Any:
    return message.answer(text="<b>❓ Usage »</b> <code>/nickname [new_nickname]</code>")
