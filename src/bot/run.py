import asyncio
from aiogram import Bot, Dispatcher
from settings import config
import logging

bot = Bot(token=config.TG_BOT_API_KEY)
dispatcher = Dispatcher()

async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
