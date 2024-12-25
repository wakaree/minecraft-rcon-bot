from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, User

from app.controllers.user import whitelist
from app.telegram.filters.whitelist import WhitelistCommandFilter
from app.telegram.helpers.text import answer_usage

if TYPE_CHECKING:
    from app.models.config import AppConfig
    from app.models.dto.user import UserDto
    from app.services.database import Database
    from app.services.rcon import RCONClient

router: Final[Router] = Router(name=__name__)


@router.message(WhitelistCommandFilter())
async def whitelist_user(
    message: Message,
    action: str,
    nickname: Optional[str],
    database: Database,
    rcon: RCONClient,
    config: AppConfig,
) -> Any:
    aiogram_user: User = message.reply_to_message.from_user
    try:
        user: UserDto = whitelist(
            user_id=aiogram_user.id,
            username=aiogram_user.username,
            nickname=nickname,
            add=action == "add",
            database=database,
            rcon=rcon,
            config=config,
        )
    except ValueError:
        return message.answer("<b>❌ Error »</b> <code>Missing player nickname</code>")
    return message.answer(
        text="<b>✉️ Whitelist »</b> <code>{nickname}</code> is now {whitelisted}".format(
            nickname=user.nickname,
            whitelisted="✅ whitelisted" if user.whitelisted else "❌ not whitelisted",
        )
    )


@router.message(Command("whitelisted"))
async def show_whitelisted_users(message: Message, database: Database) -> Any:
    users: list[UserDto] = database.get_whitelisted()
    if not users:
        return message.answer("<b>❌ Error »</b> <code>No whitelisted users</code>")
    return message.answer(
        text="<b>📋 Whitelisted users »</b>\n{users}".format(
            users="\n".join(
                "- <code>{nickname}</code> (@{username})".format(
                    nickname=user.nickname,
                    username=user.username,
                )
                for user in users
            ),
        )
    )


@router.message(Command("whitelist"))
async def answer_whitelist_usage(message: Message) -> Any:
    return answer_usage(
        message=message,
        command="whitelist [add/del] [optional:nickname]",
        must_reply=True,
    )
