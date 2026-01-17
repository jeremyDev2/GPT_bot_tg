from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())

async def message_handler(message: Message) -> None:
    await message.answer('Starting bot.')
