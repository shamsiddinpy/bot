# import re
# import logging
# import asyncio
# import os
# from typing import Tuple
# from dotenv import load_dotenv
# from aiohttp import ClientSession
# from aiogram import Bot, Dispatcher, Router, types, F
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
# from aiogram.filters import Command
#
# # 🌍 Muhit o‘zgaruvchilarni yuklash
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
#
# # 🔥 Telegram bot obyektlari
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
# router = Router()
# dp.include_router(router)
#
# # 📌 Logger sozlamalari
# logging.basicConfig(level=logging.INFO)
#
# # 📞 Telefon raqami tugmasi
# def main_phone():
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#
# # 📌 Telefon raqamini formatlash
# def format_phone_number(phone: str) -> str:
#     digits = re.sub(r'\D', '', phone)  # Faqat raqamlarni olish
#     if len(digits) == 12 and digits.startswith("998"):
#         return f"({digits[2:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"
#     return phone
#
# # 📌 Telefon raqam formatini tekshirish
# def is_valid_phone_number(number: str) -> bool:
#     pattern = re.compile(r'^\(\d{2}\)-\d{3}-\d{2}-\d{2}$')  # (XX)-XXX-XX-XX
#     return bool(pattern.match(number))
#
# async def verify_user(jshshir: str, phone: str) -> Tuple[bool, str]:
#     formatted_phone = format_phone_number(phone)
#     api_url = f"https://dev-gateway.railwayinfra.uz/api/user/jshshir/{jshshir}?project=railmap&phone={formatted_phone}"
#
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#
#     logging.info(f"APIga yuborilayotgan so‘rov: {api_url}")
#
#     try:
#         async with ClientSession() as session:
#             async with session.get(api_url, headers=headers) as response:
#                 response_text = await response.text()
#                 logging.info(f"API javobi: {response_text}")
#
#                 if response.status == 200:
#                     api_data = await response.json()
#                     user_data = api_data.get('data', {})
#                     api_phone = user_data.get('phone', '')
#                     api_jshshir = user_data.get('jshshir', '')
#
#                     if formatted_phone == api_phone:
#                         return True, f"✅ Foydalanuvchi topildi!\n📌 JSHSHIR: {api_jshshir}"
#                     else:
#                         return False, "❌ Telefon raqami mos kelmadi!"
#                 elif response.status == 404:
#                     return False, "❌ Foydalanuvchi topilmadi!"
#                 elif response.status == 401:
#                     return False, "🚫 Avtorizatsiya xatosi! Iltimos, qayta urinib ko‘ring."
#                 else:
#                     return False, "⚠️ Server xatosi! Keyinroq urinib ko‘ring."
#
#     except Exception as e:
#         logging.error(f"API so‘rovida xatolik: {str(e)}")
#         return False, f"⚠️ Texnik nosozlik! Xatolik: {str(e)}"
#
# # 🔹 /start buyrug‘i
# @router.message(Command("start"))
# async def start_command(msg: Message):
#     await msg.answer("📞 Telefon raqamingizni kiriting yoki pastdagi tugmani bosing:", reply_markup=main_phone())
#
# # 📌 Telefon raqamini tugma orqali olish
# @router.message(F.content_type == ContentType.CONTACT)
# async def handle_phone_contact(msg: Message):
#     phone_number = msg.contact.phone_number
#     await msg.answer("🔢 Iltimos, JSHSHIR raqamingizni yuboring.")
#
#     @router.message(F.text)
#     async def handle_jshshir(msg_jshshir: Message):
#         jshshir = msg_jshshir.text.strip()
#         success, message = await verify_user(jshshir, phone_number)
#         await msg_jshshir.answer(message)
#
# # 📌 Telefon raqamini qo‘lda kiritish
# @router.message(F.text)
# async def handle_manual_input(msg: Message):
#     input_data = msg.text.strip()
#
#     if is_valid_phone_number(input_data):
#         await msg.answer("🔢 Iltimos, JSHSHIR raqamingizni yuboring.")
#
#         @router.message(F.text)
#         async def handle_manual_jshshir(msg_jshshir: Message):
#             jshshir = msg_jshshir.text.strip()
#             success, message = await verify_user(jshshir, input_data)
#             await msg_jshshir.answer(message)
#     else:
#         await msg.answer("❌ Telefon raqamini (XX)-XXX-XX-XX formatda kiriting!")
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())
