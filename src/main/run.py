from settings.config import TG_BOT_API_KEY
from handlers import start
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

async def main():
    bot = Bot(token=TG_BOT_API_KEY)
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
