from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from src.settings import settings
from src.handlers import main_router
from src.tools.parse_updates import parse_updates


async def main():
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)

    @dp.startup()
    async def startup():
        logging.info("Bot started")
        asyncio.create_task(parse_updates(bot))

    @dp.shutdown()
    async def shutdown():
        logging.info("Bot stopped")

    try:
        await dp.start_polling(bot)
    except asyncio.exceptions.CancelledError:
        logging.info("The polling cycle was interrupted")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())