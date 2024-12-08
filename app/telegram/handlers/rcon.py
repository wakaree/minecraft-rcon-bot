from textwrap import dedent
from typing import Any, Final

from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.services.database import Database
from app.services.rcon import RCONClient
from app.utils.command import wrap_command

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


@router.message(Command("rcon"))
async def send_rcon_command(
    message: Message,
    command: CommandObject,
    rcon: RCONClient,
    database: Database,
) -> Any:
    if command.args is None:
        return message.answer(text="<b>❓ Usage »</b> <code>/rcon [command]</code>")
    wrapped: str = wrap_command(command=command.args, message=message, database=database)
    response: str = rcon.execute_command(wrapped)
    return message.answer(text=format_response(wrapped, response))
