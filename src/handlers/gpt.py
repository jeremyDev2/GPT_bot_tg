from pathlib import Path
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from settings import config

router = Router()

_GPT_IMAGE_: Path = config.RESOURCES_DIR / "images" / "gpt.jpg"
if not _GPT_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_GPT_IMAGE_}")

@router.message(Command("gpt"))
async def random_handler(message: Message) -> None:
    photo = FSInputFile(_GPT_IMAGE_)
    await message.answer_photo(photo=photo, caption="Asking GPT...")
