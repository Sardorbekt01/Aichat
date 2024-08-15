import asyncio
import logging
import sys
import os
from os import getenv
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, Router
from config import settings
from handlers.handlers import register_handlers
from handlers.admin_handler import register_admin_handlers
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from handlers.handlers import register_handlers, load_user_data, save_user_data  # Import qilish
from handlers.admin_handler import register_admin_handlers

BOT_TOKEN = os.getenv('BOT_TOKEN')  # API tokenni olish



bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Bot kommandalarini o'rnatish
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/profile", description="Profilni ko'rish"),
        BotCommand(command="/rejim", description="Rejim tanlash"),
        BotCommand(command="/premium", description="Premium xizmatlar"),
        BotCommand(command="/help", description="Yordam")
    ]
    await bot.set_my_commands(commands)

# Botni ishga tushirishdagi sozlashlar
async def on_startup(dp: Dispatcher):
    await set_commands(dp.bot)
    global user_usage_limits
    user_usage_limits = load_user_data()

# Botni to'xtatishda user data faylini saqlash
async def on_shutdown(dp: Dispatcher):
    save_user_data(user_usage_limits)




async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


dp = Dispatcher()

register_admin_handlers(dp)
register_handlers(dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())