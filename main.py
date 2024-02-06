import asyncio
from aiogram import Bot, Dispatcher
from configs import settings
from routers.common_router import common_router


async def main():
    dp = Dispatcher()
    dp.include_routers(common_router)
    bot = Bot(token=settings.bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
