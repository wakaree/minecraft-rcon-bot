from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.models.dto.user import UserDto
from app.services.database import Database


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")
        if user is None:
            return await handler(event, data)
        database: Database = data["database"]
        user_dto: Optional[UserDto] = database.get_user(user_id=user.id)
        if user_dto is None:
            user_dto = UserDto(id=user.id, username=user.username)
        else:
            if user_dto.username != user.username:
                user_dto.username = user.username
                database.set_user(user_dto)
        data["user"] = user_dto
        return await handler(event, data)
