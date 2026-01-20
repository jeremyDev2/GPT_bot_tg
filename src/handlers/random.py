from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message

from settings import config
from ui import keyboard

router = Router()

_RAND_IMAGE_: Path = config.RESOURCES_DIR / "images" / "random.jpg"
if not _RAND_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_RAND_IMAGE_}")

_RANDOM_PROMPT_: Path = config.RESOURCES_DIR / "prompts" / "random_prompt.txt"
if not _RANDOM_PROMPT_.is_file():
    raise FileNotFoundError(f"Random prompt not found: {_RANDOM_PROMPT_}")


@router.message(Command("random"))
async def random_handler(message: Message) -> None:
    photo = FSInputFile(_RAND_IMAGE_)
    prompt = _RANDOM_PROMPT_.read_text(encoding="utf-8").strip()
    await message.answer_photo(
        photo=photo,
        caption=prompt,
        reply_markup=keyboard.random_keyboard(),
    )


@router.callback_query(lambda call: call.data == "random")
async def random_callback(call: CallbackQuery) -> None:
    photo = FSInputFile(_RAND_IMAGE_)
    prompt = _RANDOM_PROMPT_.read_text(encoding="utf-8").strip()
    await call.message.answer_photo(
        photo=photo,
        caption=prompt,
        reply_markup=keyboard.random_keyboard(),
    )
    await call.answer()
