import logging
import os
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
from telegram.constants import ParseMode

from bot.handler.buttons.inline import main_phone, main_btn1
from bot.handler.language.language import MESSAGES
from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter, normalize_phone
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
        await msg.answer(
            MESSAGES[language]['enter_jshshir'],
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await state.update_data(jshshir=jshshir)
    await state.set_state(MainStatesGroup.main_phone)
    await msg.answer(
        text=MESSAGES[language]['enter_phone'],
        reply_markup=main_phone()
    )


@star_check_router.message(MainStatesGroup.main_phone, F.content_type == ContentType.CONTACT)
async def handle_contact(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    language = state_data.get('lang')
    jshshir = state_data.get('jshshir')

    phone_number = normalize_phone(msg.contact.phone_number)
    result = await verify_phone_number(jshshir, phone_number)

    if result is None:
        await msg.answer(
            MESSAGES[language]['technical_error'],
            reply_markup=ReplyKeyboardRemove()
        )
        return

    success, message = result
    if success:
        # Verification successful - show main menu with exit button
        await msg.answer(message, reply_markup=main_btn1(lang=language))
    else:
        # Verification failed - show error without main menu
        await msg.answer(
            message,
            reply_markup=ReplyKeyboardRemove()
        )


@star_check_router.message(MainStatesGroup.main_phone)
async def handle_phone_text(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    language = state_data.get('language', 'uz')
    phone_number = normalize_phone(msg.text.strip())

    if len(phone_number) < 9:
        await msg.answer(
            MESSAGES[language]['wrong_phone'],
            reply_markup=ReplyKeyboardRemove()
        )
        return

    jshshir = state_data.get('jshshir')
    result = await verify_phone_number(jshshir, phone_number)

    success, message = result

    if success:
        await msg.answer(
            message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=main_btn1(lang=language)
        )
    else:
        await msg.answer(
            message,
            reply_markup=ReplyKeyboardRemove()
        )
