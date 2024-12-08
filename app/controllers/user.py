from typing import Optional

from app.models.config import AppConfig
from app.models.dto.user import UserDto
from app.services.database import Database
from app.services.rcon import RCONClient


def update_nickname(
    *,
    user_id: int,
    username: Optional[str] = None,
    nickname: str,
    database: Database,
) -> tuple[Optional[str], str]:
    user: Optional[UserDto] = database.get_user(user_id=user_id)
    if user is None:
        user = UserDto(id=user_id, username=username)
    old_nickname: Optional[str] = user.nickname
    user.nickname = nickname
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
        rcon.execute_command(config.whitelist.add_command.format(user.nickname))
    else:
        rcon.execute_command(config.whitelist.remove_command.format(user.nickname))
    database.set_user(user)
    return user
