from aiogram import Router
from aiogram.types import Message
from aiograms.filters import CommandStart

my_router = Router(name=__name__)

@my_router.message(CommandStart())
async def message_handler(message: Message) -> Any:
    await message.answer('Hello from my router!')
