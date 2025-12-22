from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.filters import MasterFilter
from src.settings import settings

router = Router()
router.message.filter(MasterFilter())


@router.message(Command("start"))
async def start(message: Message):
    await message.answer_sticker(settings.start_sticker)


@router.message()
async def echo(message: Message):
    await message.answer_sticker(settings.echo_sticker)
