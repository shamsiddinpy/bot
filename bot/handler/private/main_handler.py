import logging
import os

import aiohttp
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handler.state.main_state import MainStatesGroup
from bot.handler.utls.main_jshshir_filter import is_jshshir_number_filter
from config.base import session
from config.model import TelegramUser

API_URL = "https://dev-gateway.railwayinfra.uz/api/user/jshshir/{}?project=railmap"
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


@handler_start_router.message(MainStatesGroup.main_jshshir)
async def main_handler(msg: Message, state: FSMContext):
    jshshir = msg.text.strip()
    if not is_jshshir_number_filter(jshshir):
        await msg.answer("❌ JShShIR noto‘g‘ri! U 14 xonali va faqat raqamlardan iborat bo‘lishi kerak.")
        return
    else:
        await state.set_state(MainStatesGroup.main_phone)
        await msg.answer("Telfon raqamingizni kiriting...", )

    # headers = {
    #     "Authorization": f"Bearer {API_TOKEN}"
    # }
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(API_URL.format(jshshir), headers=headers) as response:
    #         response_text = await response.text()
    #         print(response_text)
    #         if response.status == 200:
    #             json_response = await response.json()
    #             data = json_response.get("data", {})
    #             if not data:
    #                 await msg.answer("❌ Ma'lumot topilmadi.")
    #                 return
    #             fullname = data.get("fullname", " ")
    #             firstname = data.get("firstname", " ")
    #             lastname = data.get("lastname", " ")
    #             middlename = data.get("middlename", " ")
    #             birthday = data.get("birthday", " ")
    #             phone = data.get("phone", " ")
    #             birth_place = data.get("birthPlace", " ")
    #             current_place = data.get("currentPlace", " ")
    #             education = data.get("education", " ")
    #             nationality = data.get("nationality", " ")
    #             avatar = data.get("avatar", None)
    #             domain = data.get("domain", "")
    #             avatar_url = f"{domain}/{avatar}" if avatar else "Rasm mavjud emas"
    #
    #             await msg.answer(f"✅ **Foydalanuvchi ma'lumotlari**\n\n"
    #                              f"👤 **To‘liq ismi:** {fullname}\n"
    #                              f"📝 **Ism:** {firstname}\n"
    #                              f"📝 **Familiya:** {lastname}\n"
    #                              f"📝 **Otasining ismi:** {middlename}\n"
    #                              f"🎂 **Tug‘ilgan sana:** {birthday}\n"
    #                              f"📞 **Telefon:** {phone}\n"
    #                              f"📍 **Tug‘ilgan joyi:** {birth_place}\n"
    #                              f"🏠 **Hozirgi yashash joyi:** {current_place}\n"
    #                              f"📚 **Ta’lim:** {education}\n"
    #                              f"🌎 **Millati:** {nationality}\n"
    #                              f"🖼 **Rasm:** {avatar_url}", parse_mode="Markdown"
    #                              )
    #
    #             await state.update_data(user_data=data)
    #             await state.set_state(None)
    #         else:
    #             await msg.answer(f"❌ Foydalanuvchi topilmadi. Xatolik: {response_text}")
