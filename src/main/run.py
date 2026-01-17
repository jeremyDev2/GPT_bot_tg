import asyncio
from settings.config import TG_BOT_API_KEY
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from handlers import start,random

async def main():
    bot = Bot(token=TG_BOT_API_KEY)
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    dispatcher.include_router(random.router)
    await dispatcher.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())

