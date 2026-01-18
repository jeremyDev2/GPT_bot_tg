from pathlib import Path
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from settings import config

router = Router()

_QUIZ_IMAGE_: Path = config.RESOURCES_DIR / "images" / "quiz.jpg"
if not _QUIZ_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_QUIZ_IMAGE_}")

@router.message(Command("quiz"))
async def random_handler(message: Message) -> None:
    photo = FSInputFile(_QUIZ_IMAGE_)
    await message.answer_photo(photo=photo, caption="Quiz...")
