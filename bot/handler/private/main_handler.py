import logging
import os

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handler.state.main_state import MainStatesGroup
from config.base import session
from config.model import TelegramUser

API_URL = os.environ.get("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

handler_start_router = Router()
logging.basicConfig(level=logging.INFO)


@handler_start_router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    telegram_id = msg.from_user.id
    user_id = msg.from_user.username
    last_name = msg.from_user.last_name
    first_name = msg.from_user.first_name
    user_int_db = session.query(TelegramUser).filter(TelegramUser.telegram_id == telegram_id).first()

    if not user_int_db:
        new_user = TelegramUser(
            telegram_id=telegram_id,
            username=user_id,
            first_name=first_name,
            last_name=last_name,

        )
        session.add(new_user)
        session.commit()
    await state.set_state(MainStatesGroup.main_jshshir)
    await msg.answer("JSHSHIR Raqamingizni kiriting...")
