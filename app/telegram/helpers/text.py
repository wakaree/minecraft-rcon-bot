from typing import Any

from aiogram.types import Message


def usage(command: str, must_reply: bool = False) -> str:
    message: str = f"<b>❓ Usage »</b> <code>/{command}</code>"
    if must_reply:
        message += "\n<b>☝️ Message must be a reply!</b>"
    return message


def answer_usage(message: Message, command: str, must_reply: bool = False) -> Any:
    return message.answer(text=usage(command, must_reply))
