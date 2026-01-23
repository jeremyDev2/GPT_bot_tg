from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from settings import config
from ui import keyboard

router = Router()

_START_IMAGE_: Path = config.RESOURCES_DIR / "images" / "main.jpg"
if not _START_IMAGE_.is_file():
    raise FileNotFoundError(f"Start image not found: {_START_IMAGE_}")

_WELCOME_TEXT_: Path = config.RESOURCES_DIR / "welcome_text" / "main.txt"
if not _WELCOME_TEXT_.is_file():
    raise FileNotFoundError(f"Welcome text not found: {_WELCOME_TEXT_}")


@router.message(CommandStart())
async def message_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    photo = FSInputFile(_START_IMAGE_)
    welcome_text = _WELCOME_TEXT_.read_text(encoding="utf-8")
    await message.answer_photo(
        photo=photo,
        caption=welcome_text,
        reply_markup=keyboard.main_keyboard(),
    )


@router.callback_query(lambda call: call.data == "start")
async def start_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    photo = FSInputFile(_START_IMAGE_)
    welcome_text = _WELCOME_TEXT_.read_text(encoding="utf-8")
    await call.message.answer_photo(
        photo=photo,
        caption=welcome_text,
        reply_markup=keyboard.main_keyboard(),
    )
    await call.answer()
