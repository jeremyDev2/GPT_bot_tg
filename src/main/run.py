import asyncio
import logging
from settings.config import TG_BOT_API_KEY
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from handlers import start,random,talk,quiz,gpt,translator
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    bot = Bot(token=TG_BOT_API_KEY)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(start.router)
    dispatcher.include_router(random.router)
    dispatcher.include_router(talk.router)
    dispatcher.include_router(quiz.router)
    dispatcher.include_router(gpt.router)
    dispatcher.include_router(translator.router)
    await dispatcher.start_polling(bot)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__": asyncio.run(main())

