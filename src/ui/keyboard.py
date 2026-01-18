from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_keyboard():
    kb_list = [
        [KeyboardButton(text="🗣️ Talk to GPT"), KeyboardButton(text="🧠 Quiz")],
        [KeyboardButton(text="💡 Random fact"), KeyboardButton(text="📸Speak with celebrity")], [KeyboardButton(text="🔠 Translator")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True,
                                   input_field_placeholder="Menu"
                                   )
    return keyboard
