import logging
import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType

from bot.handler.utls.verify_phone_number import verify_phone_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from bot.handler.buttons.inline import main_phone
from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
star_check_router = Router()


@star_check_router.message(MainStatesGroup.main_jshshir)
async def main_handler(msg: Message, state: FSMContext):
    jshshir = msg.text.strip()
    if not is_jshshir_number_filter(jshshir):
        await msg.answer("❌ JShShIR noto‘g‘ri! U 14 xonali va faqat raqamlardan iborat bo‘lishi kerak.")
        return
    else:
        await state.set_state(MainStatesGroup.main_phone)
        await msg.answer("Telfon raqamingizni kiriting...", reply_markup=main_phone())


@star_check_router.message(MainStatesGroup.main_phone, F.content_type == ContentType.CONTACT)
async def main_handler(msg: Message, state: FSMContext):
    phone_number = msg.contact.phone_number
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg2LCJpYXQiOjE3MzgzMDI5MjEsImV4cCI6MTczODM4OTMyMX0.v-6t99or0stHlm6bJsTi1mibAtb7nY0MfEFY2XiBd74"  # O'zingizning access tokeningizni kiriting
    success, message = await verify_phone_number(phone_number, access_token)
    await msg.answer(message)
