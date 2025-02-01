import json
import os
from asyncio.log import logger
from typing import Tuple

from aiohttp import ClientSession

from bot.handler.utls.main_jshshir_filter import format_phone_number, normalize_phone

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if not ACCESS_TOKEN:
    logger.error("ACCESS_TOKEN is not set in environment variables!")
    raise ValueError("ACCESS_TOKEN is not set in environment variables!")


def format_positions(positions_str: str) -> str:
    try:
        positions = json.loads(positions_str)
        formatted_positions = []
        for pos in positions:
            org = pos.get('organization', {}).get('name', '')
            dept = pos.get('department', {}).get('name', '')
            position = pos.get('position', '')
            formatted_positions.append(f"Tashkilot: {org}\nBo'lim: {dept}\nLavozim: {position}")
        return "\n\n".join(formatted_positions)
    except:
        return positions_str


async def format_user_data(data: dict) -> str:
    if not data:
        return "Ma'lumot topilmadi"

    sections = [
        "👤 SHAXSIY MA'LUMOTLAR",
        f"To'liq ism: {data.get('fullname')}\n",
        f"Telefon: {data.get('phone')}\n",
        "\n💼 ISH MA'LUMOTLARI\n"
    ]

    positions = format_positions(data.get('positions', '[]'))
    if positions:
        sections.append(positions)

    return "\n".join(sections)


async def verify_phone_number(jshshir: str, phone: str) -> Tuple[bool, str]:
    formatted_phone = format_phone_number(phone)
    normalized_input_phone = normalize_phone(phone)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with ClientSession() as session:
            api_url = f"https://dev-gateway.railwayinfra.uz/api/user/jshshir/{jshshir}?project=railmap&phone={formatted_phone}"
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    api_data = await response.json()
                    user_data = api_data.get('data', {})

                    if user_data:
                        api_phone = normalize_phone(user_data.get('phone', ''))
                        if normalized_input_phone != api_phone:
                            return False, "❌ Kiritilgan telefon raqami ushbu JSHSHIR egasining telefon raqamiga mos kelmaydi!"
                        formatted_message = await format_user_data(user_data)
                        return True, f"✅ Foydalanuvchi ma'lumotlari topildi:\n\n{formatted_message}"
                    else:
                        return False, "❌ Ma'lumotlar topilmadi!"
                elif response.status == 404:
                    return False, "❌ Sizning ma'lumotlaringiz bazada mavjud emas!"

    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return False, "⚠️ Tizimda texnik nosozlik! Iltimos, keyinroq urinib ko'ring."
