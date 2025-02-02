import logging
import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from bot.handler.language.language import MESSAGES
from bot.handler.buttons.inline import main_phone
from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter, format_phone_number
from bot.handler.utls.verify_phone_number import verify_phone_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if not ACCESS_TOKEN:
    logger.error("ACCESS_TOKEN is not set in environment variables!")
    raise ValueError("ACCESS_TOKEN is not set in environment variables!")

star_check_router = Router()


@star_check_router.message(MainStatesGroup.main_jshshir)
async def main_handler(msg: Message, state: FSMContext):
    jshshir = msg.text.strip()
    state_data = await state.get_data()
    language = state_data.get('language', 'uz')
    if not is_jshshir_number_filter(jshshir):
        await msg.answer(msg[language]['main_jshshir'])
        return
    await state.update_data(jshshir=jshshir)
    await state.set_state(MainStatesGroup.main_phone)
    await msg.answer(text=MESSAGES[language]['enter_phone'], reply_markup=main_phone())


@star_check_router.message(MainStatesGroup.main_phone, F.content_type == ContentType.CONTACT)
async def handle_contact(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    language = state_data.get('language', 'uz')
    jshshir = state_data.get('jshshir')

    phone_number = msg.contact.phone_number
    success, message = await verify_phone_number(jshshir, phone_number)
    await msg.answer(message)


@star_check_router.message(MainStatesGroup.main_phone)
async def handle_phone_text(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    language = state_data.get('language', 'uz')

    phone_number = msg.text.strip()
    if not format_phone_number(phone_number):
        await msg.answer(MESSAGES[language]['wrong_phone'])
        return

    jshshir = state_data.get('jshshir')
    success, message = await verify_phone_number(jshshir, phone_number)
    await msg.answer(message)
