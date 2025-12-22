from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.settings import settings


class MasterFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == settings.tg_id
