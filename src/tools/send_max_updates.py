import logging

from aiogram import Bot

from src.green_api_service.green_api_service import GreenApiService
from src.models import TextMessageModel, FileMessageModel, FileType
from src.settings import settings


async def send_max_updates(bot: Bot):
    async for msg in GreenApiService.messages_generator():
        if isinstance(msg, TextMessageModel):
            text = f"<b>{msg.chat_name} - {msg.sender_name}:</b>\n\n{msg.text}"
            await bot.send_message(settings.tg_id, text)
            logging.debug(f"Message sent: {text}")
        if isinstance(msg, FileMessageModel):
            text = f"<b>{msg.chat_name} - {msg.sender_name}:</b>\n\n{msg.caption}"

            file_url = msg.file_url
            if not file_url:
                await bot.send_message(settings.tg_id, text + "<i>Файл не отправлен</i>")
                logging.debug(f"File message without url: {text}")
                continue

            if msg.file_type == FileType.IMAGE:
                await bot.send_photo(settings.tg_id, file_url, caption=text)
                logging.debug(f"Image message sent: {text}\n{file_url}")

            elif msg.file_type == FileType.VIDEO: # now send as file
                await bot.send_video(settings.tg_id, file_url, caption=text)
                # await bot.send_document(settings.tg_id, file_url, caption=text)
                logging.debug(f"Video message sent: {text}\n{file_url}")

            elif msg.file_type == FileType.DOCUMENT:
                await bot.send_document(settings.tg_id, file_url, caption=text)
                logging.debug(f"Document message sent: {text}\n{file_url}")

            elif msg.file_type == FileType.AUDIO: # now send as file
                await bot.send_voice(settings.tg_id, file_url, caption=text)
                logging.debug(f"Audio message sent: {text}\n{file_url}")
