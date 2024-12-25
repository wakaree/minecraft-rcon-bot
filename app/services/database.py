import sqlite3
from typing import Optional

from app.models.dto.user import UserDto


class Database:
    def __init__(self, filename: str = ".db") -> None:
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def startup(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT DEFAULT NULL,
                nickname TEXT DEFAULT NULL,
                whitelisted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    def shutdown(self) -> None:
        self.connection.close()

    def set_user(self, user: UserDto) -> None:
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO users (id, username, nickname, whitelisted)
            VALUES (?, ?, ?, ?);
            """,
            user.tuple(),
        )
        self.connection.commit()

    def get_user(self, user_id: int) -> Optional[UserDto]:
        self.cursor.execute(
            """
            SELECT * FROM users WHERE id = ?;
            """,
            (user_id,),
        )
        user = self.cursor.fetchone()
        return UserDto(*user) if user else None

    def by_username(self, username: str) -> Optional[UserDto]:
        self.cursor.execute(
            """
            SELECT * FROM users WHERE username = ?;
            """,
            (username,),
        )
        user = self.cursor.fetchone()
        return UserDto(*user) if user else None

    def get_whitelisted(self) -> list[UserDto]:
        self.cursor.execute(
            """
            SELECT * FROM users WHERE whitelisted = TRUE;
            """
        )
        return [UserDto(*user) for user in self.cursor.fetchall()]
