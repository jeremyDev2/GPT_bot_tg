from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_keyboard() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="🗣️ Talk to GPT"), KeyboardButton(text="🧠 Quiz")],
        [KeyboardButton(text="💡 Random fact"), KeyboardButton(text="📸Speak with celebrity")],
        [KeyboardButton(text="🔠 Translator")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Menu",
    )


def keyboard_constructor(mapping:dict[str,str], 
                         width: int = 2) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=label, callback_data=key)
        for key, label in mapping.items()
    ]
    rows = [buttons[i:i + width] for i in range(0, len(buttons), width)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def random_keyboard() -> InlineKeyboardMarkup:
    return keyboard_constructor(
        {"random_fact":"More facts!", "start": "Exit"},
        width = 1,
    )

def quiz_keyboard() -> InlineKeyboardMarkup:
    return keyboard_constructor(
        {"quiz":"More questions!", "start":"Exit"},
        width = 1,
    )

def gpt_talk_keyboard()-> InlineKeyboardMarkup:
    return keyboard_constructor(
        {"start":"Exit"},
        width = 1,
    )

def celebrity_talk_keyboard() -> InlineKeyboardMarkup:
    return keyboard_constructor(
        {"talk_cobain":"Talk to Kurt Cobain" ,"talk_hawking":"Talk to Steven Hawking", "talk_nietzsche":"Talk to Friedrich Nietzsche", "talk_queenea":"Talk to queen", "talk_tolkien":"Talk to John Tolkien", "start": "Exit"},
        width = 2
    )

def translator_keyboard() -> InlineKeyboardMarkup:
    return keyboard_constructor(
        {"translate_change_lang": "Change language", "start": "Exit"},
        width = 1,
    )

