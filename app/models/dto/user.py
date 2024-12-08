from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from app.utils.time import datetime_now


@dataclass
class UserDto:
    id: int
    username: Optional[str] = None
    nickname: Optional[str] = None
    whitelisted: bool = False
    created_at: datetime = datetime_now()

    def tuple(self) -> tuple[Any, ...]:
        return self.id, self.username, self.nickname, self.whitelisted
