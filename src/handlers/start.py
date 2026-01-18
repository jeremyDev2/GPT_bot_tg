from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from settings import config
from ui import keyboard

router = Router()

_START_IMAGE_: Path = config.RESOURCES_DIR / "images" / "main.jpg"
if not _START_IMAGE_.is_file():
    raise FileNotFoundError(f"Start image not found: {_START_IMAGE_}")

@router.message(CommandStart())
async def message_handler(message: Message) -> None:
    photo = FSInputFile(_START_IMAGE_)
    await message.answer_photo(
        photo=photo,
        caption="Starting bot.",
        reply_markup=keyboard.main_keyboard(),
    )
