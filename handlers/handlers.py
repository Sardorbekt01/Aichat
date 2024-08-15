from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta
import json
import os
from messages import MESSAGES
from commands.keyboards import mode_selection_keyboard
from controllers.gpt_controller import get_gpt4_mini_response, get_gpt4_response
from controllers.image_controller import generate_image
from controllers.tts_controller import generate_tts
from .admin_handler import register_admin_handlers, admin_panel

class Form(StatesGroup):
    mode = State()

# Foydalanuvchi ma'lumotlarini yuklash va saqlash
USER_DATA_FILE = 'user_data.json'
ADMIN_ID = os.getenv("ADMIN_ID")

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_user_limits(user_id):
    if user_id not in user_usage_limits:
        user_usage_limits[user_id] = {
            "gpt4_mini_limit": 0,
            "gpt4_limit": 0,
            "image_limit": 0,
            "tts_limit": 0,
            "joined_at": datetime.now().isoformat()
        }
        save_user_data(user_usage_limits)
    return user_usage_limits[user_id]

user_usage_limits = load_user_data()

def increment_usage(user_id, mode):
    limits = get_user_limits(user_id)
    if mode == "mode_chatgpt_4_mini":
        limits["gpt4_mini_limit"] += 1
    elif mode == "mode_chatgpt_4":
        limits["gpt4_limit"] += 1
    elif mode == "mode_image":
        limits["image_limit"] += 1
    elif mode == "mode_tts":
        limits["tts_limit"] += 1
    save_user_data(user_usage_limits)

def add_user_id_to_data(user_id):
    user_id = str(user_id)
    if user_id not in user_usage_limits:
        user_usage_limits[user_id] = {
            "gpt4_mini_limit": 0,
            "gpt4_limit": 0,
            "image_limit": 0,
            "tts_limit": 0,
            "joined_at": datetime.now().isoformat()
        }
        save_user_data(user_usage_limits)

async def start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    add_user_id_to_data(user_id)
    await state.update_data(selected_mode="mode_chatgpt_4_mini")  # Default mode set to ChatGPT-4 mini
    await message.answer(MESSAGES["start"])

async def profile_command(message: Message):
    user_id = message.from_user.id
    limits = get_user_limits(user_id)
    await message.answer(MESSAGES["profile"].format(
        gpt4_mini_limit=limits["gpt4_mini_limit"],
        gpt4_limit=limits["gpt4_limit"],
        image_limit=limits["image_limit"],
        tts_limit=limits["tts_limit"],
        obuna_turi="Bepul"
    ))

async def rejim_command(message: Message, state: FSMContext):
    await message.answer(MESSAGES["rejim"], reply_markup=mode_selection_keyboard())
    await state.set_state(Form.mode)

async def premium_command(message: Message):
    await message.answer(MESSAGES["premium"])

async def help_command(message: Message):
    await message.answer(MESSAGES["help"])

async def mode_selection_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    mode = callback_query.data
    user_id = callback_query.from_user.id
    increment_usage(user_id, mode)

    if mode == "mode_chatgpt_4_mini":
        response_text = "ChatGPT-4 mini: Hi, I'm ChatGPT-4 mini. How can I help you?"
    elif mode == "mode_chatgpt_4":
        response_text = "ChatGPT-4: Hi, I'm ChatGPT-4. How can I assist you?"
    elif mode == "mode_image":
        response_text = "Rasm yaratish: Siz tasvir yaratish rejimini tanladingiz."
    elif mode == "mode_tts":
        response_text = "Ovozli xabar: Siz ovozli xabarlar rejimini tanladingiz."
    else:
        response_text = "Noma'lum rejim tanlandi."

    await state.update_data(selected_mode=mode)
    await callback_query.message.answer(response_text)
    await callback_query.answer()

async def mode_message_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    selected_mode = user_data.get("selected_mode", "mode_chatgpt_4_mini")  # Default to ChatGPT-4 mini

    if selected_mode == "mode_chatgpt_4_mini":
        response = await get_gpt4_mini_response(message.text)
        await message.answer(response)
    elif selected_mode == "mode_chatgpt_4":
        response = await get_gpt4_response(message.text)
        await message.answer(response)
    elif selected_mode == "mode_image":
        response = await generate_image(message.text)
        await message.answer_photo(response)
    elif selected_mode == "mode_tts":
        audio = await generate_tts(message.text)
        await message.answer_voice(audio)
    else:
        response = "Noma'lum rejim tanlandi."
        await message.answer(response)


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, CommandStart())
    dp.message.register(profile_command, Command(commands=['profile']))
    dp.message.register(rejim_command, Command(commands=['rejim']))
    dp.message.register(premium_command, Command(commands=['premium']))
    dp.message.register(help_command, Command(commands=['help']))
    dp.callback_query.register(mode_selection_callback_handler, lambda c: c.data and c.data.startswith("mode_"))
    dp.message.register(mode_message_handler, StateFilter(Form.mode))
    dp.message.register(mode_message_handler, lambda m: True)
