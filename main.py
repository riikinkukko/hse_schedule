import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config
from handlers import menu_router, command_router, other_router


async def main():
    logging.basicConfig(level=logging.INFO)
    config: Config = load_config()

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_routers(command_router,
                       menu_router,
                       other_router)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())