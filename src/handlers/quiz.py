from pathlib import Path
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command, StateFilter

from services import openai
from settings import config
from ui import keyboard
from state.states import QuizState

router = Router()

_QUIZ_IMAGE_: Path = config.RESOURCES_DIR / "images" / "quiz.jpg"
if not _QUIZ_IMAGE_.is_file():
    raise FileNotFoundError(f"Quiz image not found: {_QUIZ_IMAGE_}")

@router.message(Command("quiz"))
async def quiz_handler(message: Message, state: FSMContext) -> None:
    photo = FSInputFile(_QUIZ_IMAGE_)
    await message.answer_photo(photo=photo, 
                               caption="Quiz!", 
                               reply_markup=keyboard.quiz_keyboard())
    await state.set_state(QuizState.choosing_topic)

@router.callback_query(F.data.startswith("topic_"))
async def quiz_callback(call:CallbackQuery, state:FSMContext) -> None:
    topic = call.data.replace("topic_", "")
    data= await state.get_data()
    
    if "correct" not in data or "total" not in data:
        await state.update_data(correct=0,total=0)

    await state.update_data(topic=topic)

    question = await openai.generate_text(
        system_text = "Ти генеруєш питання для квізу, але заздалегідь не давай правильной відповіді",
        user_text = f"Згенеруй 1 питання по темі {topic}.",
   ) 
    await state.update_data(last_question=question)
    await call.message.answer(question)
    await state.set_state(QuizState.waiting_answer)
    await call.answer()


@router.message(StateFilter(QuizState.waiting_answer))
async def quiz_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    question = data["last_question"]
    topic = data["topic"]
    user_text = message.text
    check = await openai.generate_text(
        system_text="Ти перевіряєш відповіді, але заздалегідь не давай правильной відповіді",
        user_text=f"Тема: {topic}. Питання: {question}. Відповідь: {user_text}. "
                  f"Відповідай тільки CORRECT або WRONG і коротке пояснення.",
    )

    correct = data["correct"]
    total = data["total"] + 1

    is_correct = check.strip().upper().startswith("CORRECT")
    if is_correct:
        correct += 1

    await state.update_data(correct=correct, total=total)
    await message.answer(
        f"{check}\nРахунок: {correct}/{total}",
        reply_markup=keyboard.quiz_keyboard(),
    )

@router.message(F.text == "🧠 Quiz")
async def menu_quiz(message: Message, state:FSMContext):
    await quiz_handler(message, state)

