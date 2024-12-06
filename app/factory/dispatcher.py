from __future__ import annotations

from aiogram import Dispatcher, F
from aiogram.filters import MagicData

from app.models.config import AppConfig
from app.services.rcon import RCONClient
from app.telegram.handlers import lifespan, rcon, start, whitelist


def create_dispatcher(config: AppConfig) -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        config=config,
        rcon=RCONClient(
            host=config.rcon.host,
            port=config.rcon.port,
            password=config.rcon.password.get_secret_value(),
        ),
    )
    dispatcher.include_routers(
        rcon.router,
        start.router,
        whitelist.router,
        lifespan.router,
    )
    dispatcher.message.filter(MagicData(F.event_from_user.id.in_(F.config.telegram.admins)))
    return dispatcher
