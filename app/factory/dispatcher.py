from __future__ import annotations

from aiogram import Dispatcher, F
from aiogram.filters import MagicData

from app.models.config import AppConfig
from app.services.database import Database
from app.services.rcon import RCONClient
from app.telegram.handlers import lifespan, nickname, rcon, start, whitelist
from app.telegram.middlewares.user import UserMiddleware


def create_dispatcher(config: AppConfig) -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        config=config,
        rcon=RCONClient(
            host=config.rcon.host,
            port=config.rcon.port,
            password=config.rcon.password.get_secret_value(),
        ),
        database=Database(),
    )
    dispatcher.include_routers(
        start.router,
        lifespan.router,
        nickname.router,
        whitelist.router,
        rcon.router,
    )
    dispatcher.message.filter(MagicData(F.event_from_user.id.in_(F.config.telegram.admins)))
    dispatcher.update.outer_middleware(UserMiddleware())
    return dispatcher
