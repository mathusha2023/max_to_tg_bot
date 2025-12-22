import asyncio
import logging

from aiogram import Bot
from src.tools.send_max_updates import send_max_updates


async def parse_updates(bot: Bot, delay=5):
    logging.debug("Start parsing updates")
    while True:
        await asyncio.sleep(delay) # seconds
        await send_max_updates(bot)
