from dataclasses import dataclass
from typing import Optional

from aiogram.enums import MessageEntityType
from aiogram.types import Message, MessageEntity

from app.models.dto.user import UserDto
from app.services.database import Database


@dataclass
class MentionedUser:
    id: int
    name: str


def extract_mentions(message: Message) -> list[str | MentionedUser]:
    text: Optional[str] = message.text or message.caption
    entities: Optional[list[MessageEntity]] = message.entities or message.caption_entities
    if not text or not entities:
        return []
    mentions: list[str | MentionedUser] = []
    for entity in entities:
        if entity.type == MessageEntityType.MENTION:
            mentions.append(entity.extract_from(text))
        elif entity.type == MessageEntityType.TEXT_MENTION and entity.user is not None:
            mentions.append(MentionedUser(id=entity.user.id, name=entity.extract_from(text)))
    return mentions


def set_nickname(command: str, target: str, user: Optional[UserDto] = None) -> str:
    if user is None or user.nickname is None:
        return command
    return command.replace(target, user.nickname)


def wrap_command(
    command: str,
    message: Message,
    database: Database,
) -> str:
    if (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and "$r" in command
    ):
        command = set_nickname(
            command=command,
            target="$r",
            user=database.get_user(message.reply_to_message.from_user.id),
        )
    for mention in extract_mentions(message):
        if isinstance(mention, MentionedUser):
            command = set_nickname(
                command=command,
                target=mention.name,
                user=database.get_user(mention.id),
            )
        if isinstance(mention, str):
            command = set_nickname(
                command=command,
                target=mention,
                user=database.by_username(mention[1:]),
            )
    return command
