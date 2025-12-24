import asyncio
import logging

from aiogram import Bot

from src.settings import settings
from src.tools.send_max_updates import send_max_updates


async def parse_updates(bot: Bot, delay=5):
    logging.debug("Start parsing updates")
    while True:
        await asyncio.sleep(delay) # seconds
        try:
            await send_max_updates(bot)
        except Exception as e:
            logging.error(f"Error in parse_updates: {e}")
            await bot.send_message(settings.tg_id, f"Error in parse_updates: {e}!!!!")
