from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class GptState(StatesGroup):
    waiting_question = State()

class QuizState(StatesGroup):
    choosing_topic = State()
    waiting_answer = State()

class TalkState(StatesGroup):
    choosing_personality = State()
    waiting_answer = State()
    user_speaks = State()

class TranslatorState(StatesGroup):
    user_text = State()
    translate_text = State()
