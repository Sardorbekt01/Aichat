from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mode_selection_keyboard():
    buttons = [
        InlineKeyboardButton(text="ChatGPT-4-mini", callback_data="mode_chatgpt_4_mini"),
        InlineKeyboardButton(text="ChatGPT-4", callback_data="mode_chatgpt_4"),
        InlineKeyboardButton(text="Rasm yaratish", callback_data="mode_image"),
        InlineKeyboardButton(text="Ovozli xabar", callback_data="mode_tts"),
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard