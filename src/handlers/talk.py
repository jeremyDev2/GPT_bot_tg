from pathlib import Path
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command, StateFilter

from state.states import TalkState
from settings import config
from services import openai
from ui.keyboard import celebrity_talk_keyboard 

router = Router()

_TALK_IMAGE_: Path = config.RESOURCES_DIR / "images" / "talk.jpg"
if not _TALK_IMAGE_.is_file():
    raise FileNotFoundError(f"Talk image not found: {_TALK_IMAGE_}")

PROMPTS = {
    "talk_cobain": "talk_cobain.txt",
    "talk_hawking": "talk_hawking.txt",
    "talk_nietzsche": "talk_nietzsche.txt",
    "talk_queenea": "talk_queenea.txt",
    "talk_tolkien": "talk_tolkien.txt",
}

@router.message(Command("talk"))
async def talk_handler(message: Message, state:FSMContext) -> None:
    photo = FSInputFile(_TALK_IMAGE_)
    await message.answer_photo(photo=photo, 
                               caption="Select famouse person", 
                               reply_markup=celebrity_talk_keyboard())
    await state.set_state(TalkState.choosing_personality)

@router.callback_query(F.data.startswith("talk_"))
async def talk_callback(call: CallbackQuery, state: FSMContext) -> None:
    filename = PROMPTS[call.data]
    prompt_path = config.RESOURCES_DIR / "prompts" / f"{filename}"
    system_text = prompt_path.read_text(encoding='utf-8')
    
    await state.update_data(personality_prompt=system_text)
    await state.set_state(TalkState.waiting_answer)

    await call.message.answer("Send message")
    await call.answer()

@router.message(StateFilter(TalkState.waiting_answer))
async def talk_message(message: Message, state: FSMContext):
    data = await state.get_data()
    system_text = data["personality_prompt"]
    user_text = message.text
    answer = await openai.generate_text(system_text, user_text)
    await message.answer(answer)

@router.message(F.text == "📸Speak with celebrity")
async def menu_talk(message: Message, state: FSMContext):
    await talk_handler(message, state)

