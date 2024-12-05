from textwrap import dedent
from typing import Any, Final

from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.services.rcon import RCONClient

router: Final[Router] = Router(name=__name__)


def format_response(command: str, response: str) -> str:
    cmd_string: str = dedent(
        """
        <b>💻 Command »</b>
        <pre><code class="language-minecraft">{command}</code></pre>
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
) -> Any:
    if command.args is None:
        return message.answer(text="<b>❓ Usage »</b> <code>/rcon [command]</code>")
    response: str = await rcon.execute_command(command.args)
    return message.answer(text=format_response(command.args, response))
