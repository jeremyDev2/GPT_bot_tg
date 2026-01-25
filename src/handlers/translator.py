from pathlib import Path
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command, StateFilter
from services import openai

from settings import config
from state.states import TranslatorState
from ui.keyboard import translator_keyboard

router = Router()

_TRANSLATOR_IMAGE_: Path = config.RESOURCES_DIR / "images" / "translator.jpg"
if not _TRANSLATOR_IMAGE_.is_file():
    raise FileNotFoundError(f"Translator image not found: {_TRANSLATOR_IMAGE_}")

@router.message(Command("translator"))
async def translator_handler(message: Message) -> None:
    photo = FSInputFile(_TRANSLATOR_IMAGE_)
    await message.answer_photo(photo=photo, 
                               caption="Send text to translate", 
                               reply_markup=translator_keyboard())

@router.callback_query(F.data.startswith("translate_to_"))
async def callback_query(call:CallbackQuery, state:FSMContext)-> None:
    lang = call.data.replace("translate_to_", "")
    await state.update_data(lang=lang)
    await state.set_state(TranslatorState.user_text)
    await call.answer()

@router.message(StateFilter(TranslatorState.user_text))
async def answer_message(message:Message, state:FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    user_text = message.text
    system_text = "You are a translator"
    answer = await openai.generate_text(system_text, f"Translate to {lang} : {user_text}")
    await message.answer(answer)

@router.message(F.text == "🔠 Translator")
async def menu_talk(message: Message, state: FSMContext):
    await translator_handler(message)

