from pathlib import Path
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from settings import config
from ui.keyboard import celebrity_talk_keyboard

router = Router()

_TALK_IMAGE_: Path = config.RESOURCES_DIR / "images" / "talk.jpg"
if not _TALK_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_TALK_IMAGE_}")

@router.message(Command("talk"))
async def talk_handler(message: Message) -> None:
    photo = FSInputFile(_TALK_IMAGE_)
    await message.answer_photo(photo=photo, caption="Select famouse person", reply_markup=celebrity_talk_keyboard())

