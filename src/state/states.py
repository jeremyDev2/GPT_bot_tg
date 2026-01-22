from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class GptState(StatesGroup):
    waiting_question = State()

class QuizState(StatesGroup):
    choosing_topic = State()
    waiting_answer = State()
