from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from services.open_ai_chat import utils, client
from aiogram import types
from enum import Enum
from bot import run

_DEFAULT: Final  = object()

async def start_callback(update, context): str:

    await update.message.reply_text(f"Welcome to GPT_bot : {version} version")

comand_handlers = CommandHandler()

main = InlineKeyboardMarkup(inline_leyboard = [])
