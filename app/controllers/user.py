from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from app.controllers.rcon import add_to_whitelist, remove_from_whitelist
from app.models.dto.user import UserDto

if TYPE_CHECKING:
    from app.models.config import AppConfig
    from app.services.database import Database
    from app.services.rcon import RCONClient


def update_nickname(
    *,
    user_id: int,
    username: Optional[str] = None,
    nickname: str,
    database: Database,
    rcon: RCONClient,
    config: AppConfig,
) -> tuple[Optional[str], str]:
    user: Optional[UserDto] = database.get_user(user_id=user_id)
    if user is None:
        user = UserDto(id=user_id, username=username)
    old_nickname: Optional[str] = user.nickname
    user.nickname = nickname
    if user.whitelisted:
        if old_nickname is not None:
            remove_from_whitelist(nickname=old_nickname, rcon=rcon, config=config)
        add_to_whitelist(nickname=user.nickname, rcon=rcon, config=config)
    database.set_user(user)
    return old_nickname, nickname


def whitelist(
    *,
    user_id: int,
    username: Optional[str] = None,
    nickname: Optional[str],
    add: bool = True,
    database: Database,
    rcon: RCONClient,
    config: AppConfig,
) -> UserDto:
    user: Optional[UserDto] = database.get_user(user_id=user_id)
    if user is None:
        user = UserDto(id=user_id, username=username)
    if user.nickname is None and nickname is None:
        raise ValueError()
    if nickname is not None and user.nickname != nickname:
        user.nickname = nickname
    user.whitelisted = add
    if add:
        add_to_whitelist(nickname=cast(str, user.nickname), rcon=rcon, config=config)
    else:
        remove_from_whitelist(nickname=cast(str, user.nickname), rcon=rcon, config=config)
    database.set_user(user)
    return user
