from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import random

from telegram import Bot

from bot.handler.buttons.inline import main_phone
from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter


star_check_router = Router()
verification_codes = {}


@star_check_router.message(MainStatesGroup.main_jshshir)
async def main_handler(msg: Message, state: FSMContext):
    jshshir = msg.text.strip()
    if not is_jshshir_number_filter(jshshir):
        await msg.answer("❌ JShShIR noto‘g‘ri! U 14 xonali va faqat raqamlardan iborat bo‘lishi kerak.")
        return
    else:
        await state.set_state(MainStatesGroup.main_phone)
        await msg.answer("Telfon raqamingizni kiriting...", reply_markup=main_phone())


@star_check_router.message(MainStatesGroup.main_phone)
async def main_handler(msg: Message, state: FSMContext):
    phone = msg.text.strip() if msg.text else None
    if not phone and msg.contact:
        phone = msg.contact.phone_number

    if len(phone) < 10 or len(phone) > 13 or not phone.isdigit():
        await msg.answer("❌ Telefon raqami noto‘g‘ri! 10-13 xonali va faqat raqamlardan iborat bo‘lishi kerak.")
        return
    verification_code = random.randint(1000, 9999)
    verification_codes[msg.from_user.id] = verification_code
    from dispatcher import bot
    await bot.send_message(chat_id=msg.chat.id,
                           text=f"✅ Tasdiqlash kodi: `{verification_code}`\n\nKodini botga yuboring.",
                           parse_mode="Markdown")
    await state.update_data(phone=phone)
    await state.set_state(MainStatesGroup.main_verify_code)
