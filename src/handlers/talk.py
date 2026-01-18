from pathlib import Path
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from settings import config

router = Router()

_TALK_IMAGE_: Path = config.RESOURCES_DIR / "images" / "talk.jpg"
if not _TALK_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_TALK_IMAGE_}")

@router.message(Command("talk"))
async def random_handler(message: Message) -> None:
    photo = FSInputFile(_TALK_IMAGE_)
    await message.answer_photo(photo=photo, caption="Talking...")
