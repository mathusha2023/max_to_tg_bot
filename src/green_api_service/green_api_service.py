import logging
from typing import AsyncGenerator

import aiohttp
from src.models import ReceiptModel, MessageFactory, MessageModel
from src.settings import settings


class GreenApiService:
    api_url = settings.api_url
    id_instance = settings.id_instance
    api_token_instance = settings.api_token_instance

    @classmethod
    async def receive_notification(cls):
        async with aiohttp.ClientSession() as session:
            url = f"{cls.api_url}/waInstance{cls.id_instance}/receiveNotification/{cls.api_token_instance}"
            async with session.get(url) as response:
                if response.status != 200: raise
                res =  await response.json()
                logging.debug(res)
                if not res: return None
                body = res["body"]
                if body["typeWebhook"] != "incomingMessageReceived":
                    await cls.delete_notification(res["receiptId"])
                    return None
                msg =  MessageFactory.from_json(body)
                return ReceiptModel(id=res["receiptId"], message=msg)

    @classmethod
    async def delete_notification(cls, receipt_id: int):
        async with aiohttp.ClientSession() as session:
            url = f"{cls.api_url}/waInstance{cls.id_instance}/deleteNotification/{cls.api_token_instance}/{receipt_id}"
            async with session.delete(url) as response:
                if response.status != 200: raise
                res =  await response.json()
                logging.debug(res)
                if not res["result"]:
                    raise

    @classmethod
    async def messages_generator(cls) -> AsyncGenerator[MessageModel, None]:
        while True:
            try:
                receipt = await cls.receive_notification()
                if receipt is None:
                    break
                yield receipt.message
                await cls.delete_notification(receipt.id)
            except Exception as e:
                logging.error(f"Error in messages_generator: {e}")
                break
