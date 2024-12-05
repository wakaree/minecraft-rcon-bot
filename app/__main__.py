from aiogram import Bot, Dispatcher

from app.factory.app_config import create_app_config
from app.factory.bot import create_bot
from app.factory.dispatcher import create_dispatcher
from app.models.config import AppConfig
from app.utils.logging import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()
    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    return dispatcher.run_polling(bot)


if __name__ == "__main__":
    main()
