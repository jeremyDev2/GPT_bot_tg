from pathlib import Path
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from settings import config

router = Router()

_RAND_IMAGE_: Path = config.RESOURCES_DIR / "images" / "random.jpg"
if not _RAND_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_RAND_IMAGE_}")

@router.message(Command("random"))
async def random_handler(message: Message) -> None:
    photo = FSInputFile(_RAND_IMAGE_)
    await message.answer_photo(photo=photo, caption="Generating fact...")
