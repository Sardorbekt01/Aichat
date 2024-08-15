from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from .change_api import *
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    awaiting_new_api_key = State()
    awaiting_limits = State()
    awaiting_broadcast_message = State()
    awaiting_new_admin_id = State()
    awaiting_mode_selection = State()
    awaiting_api_action = State()



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_USER_ID = os.getenv("ADMIN_ID")
USER_DATA_FILE = 'user_data.json'
ADMINS_FILE = 'admins.json'

router = Router()

load_dotenv()

def update_openai_api_key(new_api_key: str):
    env_path = '.env'
    set_key(env_path, 'OPENAI_API_KEY', new_api_key)
    print("API key has been updated successfully.")

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

user_usage_limits = load_user_data()

def get_user_limits(user_id):
    if str(user_id) not in user_usage_limits:
        user_usage_limits[str(user_id)] = {
            "gpt3_5_limit": 0,
            "gpt4_limit": 0,
            "image_limit": 0,
            "tts_limit": 0,
            "joined_at": datetime.now().isoformat()
        }
        save_user_data(user_usage_limits)
    return user_usage_limits[str(user_id)]

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if str(message.from_user.id) == ADMIN_USER_ID:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Statistikani ko'rsatish📝"), KeyboardButton(text="API kalitini o'zgartirish🌐")],
                [KeyboardButton(text="Kanal qo'shish📲"),KeyboardButton(text="Adminlarni qo'shish➕")],
                [KeyboardButton(text="Hamma foydalanuvchilarga xabar yuborish📩"),],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Admin paneli", reply_markup=keyboard)
    else:
        await message.answer("Sizda bu panelga kirish huquqi yo'q.")

def calculate_statistics():
    now = datetime.now()
    today = now.date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)
    
    stats = {
        "daily": 0,
        "weekly": 0,
        "monthly": 0,
        "yearly": 0,
        "all_time": len(user_usage_limits)
    }
    
    for user_id, data in user_usage_limits.items():
        joined_at = datetime.fromisoformat(data["joined_at"]).date()
        if joined_at == today:
            stats["daily"] += 1
        if joined_at >= start_of_week:
            stats["weekly"] += 1
        if joined_at >= start_of_month:
            stats["monthly"] += 1
        if joined_at >= start_of_year:
            stats["yearly"] += 1
    
    return stats

@router.message(lambda message: message.text == "Statistikani ko'rsatish📝")
async def show_stats(message: types.Message):
    if str(message.from_user.id) == ADMIN_USER_ID:
        stats = calculate_statistics()
        await message.answer(f"Statistika:\n\n"
                             f"Kunlik foydalanuvchilar: {stats['daily']}\n"
                             f"Haftalik foydalanuvchilar: {stats['weekly']}\n"
                             f"Oylik foydalanuvchilar: {stats['monthly']}\n"
                             f"Yillik foydalanuvchilar: {stats['yearly']}\n"
                             f"Butun vaqt davomida foydalanuvchilar: {stats['all_time']}")
    else:
        await message.answer("Sizda bu komandaning ishlatish huquqi yo'q.")



def get_all_user_ids():
    return list(user_usage_limits.keys())

async def send_message_to_all_users(bot: Bot, message_text: str):
    user_ids = get_all_user_ids()
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=message_text)
        except Exception as e:
            print(f"Foydalanuvchi {user_id} ga xabar yuborishda xatolik: {e}")

@router.message(lambda message: message.text == "Hamma foydalanuvchilarga xabar yuborish")
async def broadcast(message: types.Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN_USER_ID:
        await message.answer("Iltimos, barcha foydalanuvchilarga yuboriladigan xabarni yuboring.")
        await state.set_state(AdminStates.awaiting_broadcast_message)
    else:
        await message.answer("Siz ushbu panelga kirish huquqiga ega emassiz.")

@router.message(AdminStates.awaiting_broadcast_message)
async def handle_broadcast_message(message: types.Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN_USER_ID:
        broadcast_message = message.text
        await send_message_to_all_users(message.bot, broadcast_message)
        await message.answer("Xabar barcha foydalanuvchilarga yuborildi.")
        await state.clear()
    else:
        await message.answer("Siz xabar yuborish huquqiga ega emassiz.")

@router.message(lambda message: message.text == "Adminlarni qo'shish")
async def add_admin(message: types.Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN_USER_ID:
        await message.answer("Yangi adminning Telegram ID sini yuboring:")
        await state.set_state(AdminStates.awaiting_new_admin_id)
    else:
        await message.answer("Sizda adminlarni qo'shish huquqi yo'q.")

@router.message(AdminStates.awaiting_new_admin_id)
async def process_new_admin_id(message: types.Message, state: FSMContext):
    new_admin_id = message.text.strip()
    if str(message.from_user.id) == ADMIN_USER_ID:
        with open(ADMINS_FILE, 'r') as file:
            admins = json.load(file)
        if new_admin_id not in admins:
            admins.append(new_admin_id)
            with open(ADMINS_FILE, 'w') as file:
                json.dump(admins, file, indent=4)
            await message.answer(f"Yangi admin {new_admin_id} qo'shildi.")
        else:
            await message.answer("Bu foydalanuvchi allaqachon admin.")
        await state.clear()
    else:
        await message.answer("Sizda adminlarni qo'shish huquqi yo'q.")




def register_admin_handlers(dp: Dispatcher):
    # Admin panel uchun command handler
    dp.message.register(admin_panel, Command("admin"))

    # Statistika ko'rsatish handleri
    dp.message.register(show_stats, lambda message: message.text == "Statistikani ko'rsatish📝")

    # API kalitini o'zgartirish handleri
    dp.message.register(api_key_management, lambda message: message.text == "API kalitini o'zgartirish🌐")

    # Xabarni barcha foydalanuvchilarga yuborish handleri
    dp.message.register(handle_broadcast_message, lambda message: message.text == "Hamma foydalanuvchilarga xabar yuborish📩")

    # Yangi admin qo'shish handleri
    dp.message.register(process_new_admin_id, lambda message: message.text == "Adminlarni qo'shish➕")

    # API kalitlarini boshqarish handleri
    dp.callback_query.register(api_key_management, lambda callback: callback.data == "api_key_management")
    
    # Add new API key
    dp.callback_query.register(show_all_api, lambda callback: callback.data == "show_all_api")
    dp.callback_query.register(show_mode_api_history, lambda callback: callback.data.startswith("show_"))
    dp.callback_query.register(add_api_key_callback, lambda callback: callback.data == "add_api_key")
    dp.callback_query.register(process_api_addition, lambda callback: callback.data.startswith("add_"))
    
    # Set new API key
    dp.message.register(set_new_api_key, StateFilter(AdminStates.awaiting_new_api_key))
    
    # Back button functionality
    dp.callback_query.register(back_to_previous, lambda callback: callback.data in ["api_key_management", "admin"])
    
    # Registering other handlers with states
    dp.message.register(handle_broadcast_message, StateFilter(AdminStates.awaiting_broadcast_message))
    dp.message.register(process_new_admin_id, StateFilter(AdminStates.awaiting_new_admin_id))
