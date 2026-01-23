from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from settings import config
from services import openai
from state.states import GptState

router = Router()

_GPT_IMAGE_: Path = config.RESOURCES_DIR / "images" / "gpt.jpg"
if not _GPT_IMAGE_.is_file():
    raise FileNotFoundError(f"Random image not found: {_GPT_IMAGE_}")

_GPT_PROMPT_: Path = config.RESOURCES_DIR / "prompts" / "main_prompt.txt"

@router.message(Command("gpt"))
async def gpt_handler(message: Message, state: FSMContext) -> None:
    photo = FSInputFile(_GPT_IMAGE_)
    await message.answer_photo(photo=photo, caption="Asking GPT...")
    await state.set_state(GptState.waiting_question)

@router.message(StateFilter(GptState.waiting_question))
async def gpt_question(message:Message, state:FSMContext) -> None:
    system_text = _GPT_PROMPT_.read_text(encoding="utf-8").strip()
    user_text = message.text
    answer = await openai.generate_text(system_text,user_text)
    await message.answer(answer)
    if user_text == "Exit":
        await state.clear()


@router.message(F.text == "🗣️ Talk to GPT")
async def menu_gpt(message: Message, state: FSMContext):
    await gpt_handler(message, state)
