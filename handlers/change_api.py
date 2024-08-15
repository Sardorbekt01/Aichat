import os
import json
from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from dotenv import load_dotenv, set_key

load_dotenv()

ADMIN_USER_ID = os.getenv("ADMIN_ID")

router = Router()

class AdminStates(StatesGroup):
    awaiting_new_api_key = State()
    awaiting_api_action = State()
    awaiting_mode_selection = State()

# API kalitini yangilash
def update_openai_api_key(new_api_key: str):
    env_path = '.env'
    set_key(env_path, 'OPENAI_API_KEY', new_api_key)
    print("API kaliti muvaffaqiyatli yangilandi.")

def get_api_tokens():
    return {
        "gpt4_mini": os.getenv("OPENAI_API_KEY"),
        "gpt4": os.getenv("OPENAI_API_KEY"),
        "image_gen": os.getenv("IMAGE_TOKEN"),
        "tts": os.getenv("TTS_TOKEN")
    }

def load_api_history():
    history = {
        "gpt4_mini": [],
        "gpt4": [],
        "image_gen": [],
        "tts": []
    }
    
    if os.path.exists("api_history.json"):
        with open("api_history.json", "r") as file:
            history = json.load(file)
    
    return history

def save_api_history(history):
    with open("api_history.json", "w") as file:
        json.dump(history, file, indent=4)

def add_to_api_history(mode, new_api_key):
    history = load_api_history()
    if mode in history:
        history[mode].append(new_api_key)
        save_api_history(history)

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

@router.callback_query(lambda c: c.data == "api_key_management" or c.data == "admin")
async def back_to_previous(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    previous_message_id = data.get("previous_message_id")
    
    if previous_message_id:
        try:
            await callback_query.message.delete_reply_markup()
            await callback_query.bot.delete_message(callback_query.message.chat.id, previous_message_id)
        except Exception as e:
            print(f"Xabarni o'chirishda xato: {e}")

    if callback_query.data == "api_key_management":
        await api_key_management(callback_query.message, state)
    elif callback_query.data == "admin":
        await admin_panel(callback_query.message)

@router.message(lambda c: c.data == "api_key_management")
async def api_key_management(message: types.Message,state: FSMContext):
    if str(message.from_user.id) == ADMIN_USER_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Barcha APIlar", callback_data="show_all_api")],
            [InlineKeyboardButton(text="API qo'shish", callback_data="add_api_key")],
            [InlineKeyboardButton(text="Orqaga qaytish", callback_data="admin")]
        ])
        await message.answer("Botga qo'shilgan APIlar:", reply_markup=keyboard)
        await state.update_data(previous_message_id=message.message_id)
    else:
        await message.answer("Sizda bu panelga kirish huquqi yo'q")



@router.callback_query(lambda c: c.data == "show_all_api")
async def show_all_api(callback_query: types.CallbackQuery, state: FSMContext):
    if str(callback_query.from_user.id) == ADMIN_USER_ID:
        api_history = load_api_history()

        if not any(api_history.values()):
            await callback_query.message.answer("APIlar mavjud emas.")
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="GPT-4 APIlar", callback_data="show_gpt4_apis")],
                [InlineKeyboardButton(text="Image APIlar", callback_data="show_image_apis")],
                [InlineKeyboardButton(text="TTS APIlar", callback_data="show_tts_apis")],
                [InlineKeyboardButton(text="Orqaga qaytish", callback_data="admin")]
            ])

            await callback_query.message.answer("Qaysi rejimni API tarixi kerak?", reply_markup=keyboard)
            await state.update_data(previous_message_id=callback_query.message.message_id)
            await state.set_state(AdminStates.awaiting_mode_selection)
    else:
        await callback_query.message.answer("Sizda bu panelga kirish huquqi yo'q.")

@router.callback_query(AdminStates.awaiting_mode_selection)
async def show_mode_api_history(callback_query: types.CallbackQuery, state: FSMContext):
    mode_map = {
        "show_gpt4_apis": "gpt4",
        "show_image_apis": "image_gen",
        "show_tts_apis": "tts"
    }
    
    mode = mode_map.get(callback_query.data)
    if mode:
        api_history = load_api_history().get(mode, [])
        current_api = get_api_tokens().get(mode)

        if api_history:
            history_text = "\n".join(f"{i + 1}. {key}" for i, key in enumerate(api_history))
            history_text += f"\n\nHozirgi API kaliti:\n{current_api}"
            await callback_query.message.answer(f"{mode} APIlar tarixi:\n{history_text}")
        else:
            await callback_query.message.answer("APIlar mavjud emas.")

        await state.clear()
    else:
        await callback_query.message.answer("Noto'g'ri buyruq.")

@router.callback_query(lambda c: c.data == "add_api_key")
async def add_api_key_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if str(callback_query.from_user.id) == ADMIN_USER_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="GPT-4 API qo'shish", callback_data="add_gpt4_api")],
            [InlineKeyboardButton(text="Image API qo'shish", callback_data="add_image_api")],
            [InlineKeyboardButton(text="TTS API qo'shish", callback_data="add_tts_api")],
            [InlineKeyboardButton(text="Orqaga qaytish", callback_data="api_key_management")]
        ])
        await callback_query.message.answer("Qaysi rejimga API qo'shmoqchisiz?", reply_markup=keyboard)
        await state.update_data(previous_message_id=callback_query.message.message_id)
        await state.set_state(AdminStates.awaiting_api_action)
    else:
        await callback_query.message.answer("Sizda bu panelga kirish huquqi yo'q.")

@router.callback_query(AdminStates.awaiting_api_action)
async def process_api_addition(callback_query: types.CallbackQuery, state: FSMContext):
    mode_map = {
        "add_gpt4_api": "gpt4",
        "add_image_api": "image_gen",
        "add_tts_api": "tts"
    }
    
    mode = mode_map.get(callback_query.data)
    if mode:
        await callback_query.message.answer("Yangi API kalitini yuboring:")
        await state.update_data(mode=mode)
        await state.set_state(AdminStates.awaiting_new_api_key)
    else:
        await callback_query.message.answer("Noto'g'ri buyruq.")

@router.message(AdminStates.awaiting_new_api_key)
async def set_new_api_key(message: Message, state: FSMContext):
    if str(message.from_user.id) == ADMIN_USER_ID:
        new_api_key = message.text
        data = await state.get_data()
        mode = data.get("mode")

        update_openai_api_key(new_api_key)
        add_to_api_history(mode, new_api_key)

        await message.answer(f"{mode} uchun API kaliti muvaffaqiyatli yangilandi.")
        await state.clear()
    else:
        await message.answer("Sizda API kalitini o'zgartirish huquqi yo'q.")


