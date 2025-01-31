from typing import Tuple
from aiohttp import ClientSession

from bot.handler.utls.main_jshshir_filter import format_phone_number


async def verify_phone_number(phone: str, access_token: str) -> Tuple[bool, str]:
    formatted_phone = format_phone_number(phone)  # Telefon raqamini formatlash

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with ClientSession() as session:
            api_url = f"https://dev-gateway.railwayinfra.uz/api/user/phone/{formatted_phone}?project=railmap"
            print(api_url)
            async with session.get(api_url, headers=headers) as response:
                response_text = await response.text()
                print(response_text)

                if response.status == 200:
                    api_data = await response.json()

                    user_data = api_data.get('data', {})
                    api_phone = user_data.get('phone', '')
                    api_jshshir = user_data.get('jshshir', '')

                    if formatted_phone == api_phone:
                        return True, f"✅ Tabriklaymiz! Sizning telefon raqamingiz topildi, JSHSHIR: {api_jshshir}!"
                    else:
                        return False, "❌ Kechirasiz, sizning ma'lumotlaringiz mos kelmadi!"

                elif response.status == 404:
                    return False, "❌ Sizning telefon raqamingiz bazada topilmadi!"
                elif response.status == 401:
                    return False, "🚫 Tizimga kirishda xatolik! Iltimos, qaytadan urinib ko'ring."
                else:
                    return False, "⚠️ Tizimda texnik nosozlik! Iltimos, keyinroq urinib ko'ring."

    except Exception as e:
        return False, f"⚠️ Tizimda texnik nosozlik! Iltimos, keyinroq urinib ko'ring. Xatolik: {str(e)}"
