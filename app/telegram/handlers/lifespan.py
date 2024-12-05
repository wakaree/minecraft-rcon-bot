from typing import Final

from aiogram import Bot, Router, loggers
from aiogram.types import BotCommand

from app.models.config import AppConfig
from app.services.rcon import RCONClient

router: Final[Router] = Router(name=__name__)


@router.startup()
async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=config.telegram.drop_pending_updates)
    if config.telegram.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


@router.startup()
async def startup(rcon: RCONClient, bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(command="rcon", description="Execute RCON command"),
            BotCommand(command="whitelist", description="Manage whitelist"),
        ],
    )
    await rcon.client.connect()


@router.shutdown()
async def shutdown(rcon: RCONClient) -> None:
    await rcon.client.close()
