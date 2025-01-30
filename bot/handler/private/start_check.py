import json
from http.client import responses

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handler.buttons.inline import main_phone
from bot.handler.private.main_handler import API_URL
from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter

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
    formatted_phone = f"{phone_number[1:3]}-{phone_number[3:6]}-{phone_number[6:8]}-{phone_number[8:]}"
    if isinstance(API_URL['data'], str):
        print(isinstance(API_URL['data'], str))
        API_URL['data'] = json.loads(API_URL['data'])
    if formatted_phone == API_URL['data']['phone']:
        user_data = API_URL['data']
        response = (f"✅ **Foydalanuvchi ma'lumotlari**\n\n"
                    f"📝 **Ism:** {user_data['firstname']}\n"
                    f"📝 **Familiya:** {user_data['lastname']}\n"
                    f"📞 **Telefon:** {user_data['phone']}\n"
                    f"🧑‍💼 **Bo‘lim boshlig‘i** {user_data['positions']}"
                    )
        await msg.answer(response)
    else:
        await msg.answer("❌ Sizning telefon raqamingiz noto‘g‘ri!")
