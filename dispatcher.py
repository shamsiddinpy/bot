import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.handler import private_handler_router

load_dotenv()

# pip install python-dotenv
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN, )
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(private_handler_router)
