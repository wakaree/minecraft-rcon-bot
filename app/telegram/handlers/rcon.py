from __future__ import annotations

import re
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router, html
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import Command
from aiogram.types import Message

from app.telegram.helpers.text import answer_usage
from app.utils.command import wrap_command

if TYPE_CHECKING:
    from app.services.database import Database
    from app.services.rcon import RCONClient

router: Final[Router] = Router(name=__name__)


def format_response(command: str, response: str) -> str:
    cmd_string: str = dedent(
        """
        <b>💻 Command »</b>
        <pre><code>{command}</code></pre>
        """
    )
    if not response:
        cmd_string += "\n<b>✅ Executed successfully</b>"
    else:
        cmd_string += "\n<b>📝 Response »</b>\n<blockquote>{response}</blockquote>"
    return cmd_string.format(command=command, response=html.quote(response))


@router.message(Command("rcon", magic=F.args.as_("command")))
async def send_rcon_command(
    message: Message,
    command: str,
    rcon: RCONClient,
    database: Database,
) -> Any:
    wrapped: str = wrap_command(command=command, message=message, database=database)
    response: str = rcon.execute_command(wrapped)
    return message.answer(text=format_response(wrapped, response))


@router.message(Command("rcon"))
async def answer_rcon_usage(message: Message) -> Any:
    return answer_usage(message=message, command="rcon [command]")


@router.message(F.text.startswith("/"))
async def send_rcon_command_from_text(
    message: Message,
    rcon: RCONClient,
    database: Database,
) -> Any:
    if re.fullmatch(r"/\w+@.+", message.text):
        return UNHANDLED
    return await send_rcon_command(
        message=message,
        command=message.text[1:],
        rcon=rcon,
        database=database,
    )
