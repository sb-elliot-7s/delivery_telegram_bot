import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from configs import settings
from routers.common_router import common_router
from routers.admin_router import admin_router
from routers.dish_router import dish_router


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_routers(common_router, admin_router, dish_router)
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.MARKDOWN_V2)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
