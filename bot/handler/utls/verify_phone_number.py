from typing import Tuple
from aiohttp import ClientSession


async def verify_phone_number(jshshir: str, phone: str, access_token: str) -> Tuple[bool, str]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with ClientSession() as session:
            api_url = f"https://dev-gateway.railwayinfra.uz/api/user/phone{phone}?project=railmap"

            async with session.get(api_url, headers=headers) as response:
                response_text = await response.text()
                print(response_text)

                if response.status == 200:
                    api_data = await response.json()

                    # API-dan kelgan malumotlar
                    user_data = api_data.get('data', {})
                    api_phone = user_data.get('phone', '')
                    api_jshshir = user_data.get('jshshir', '')

                    # Foydalanuvchi kiritgan raqam va JSHSHIR API dagi bilan mos kelsa
                    if phone == api_phone and jshshir == api_jshshir:
                        return True, "✅ Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz!"
                    else:
                        return False, "❌ Kechirasiz, sizning ma'lumotlaringiz mos kelmadi!"

                elif response.status == 404:
                    return False, "❌ Sizning telefon raqamingiz bazada topilmadi!"
                elif response.status == 401:
                    return False, "🚫 Tizimga kirishda xatolik! Iltimos, qaytadan urinib ko'ring."
                else:
                    return False, "⚠️ Tizimda texnik nosozlik! Iltimos, keyinroq urinib ko'ring."

    except Exception as e:
        return False, "⚠️ Tizimda texnik nosozlik! Iltimos, keyinroq urinib ko'ring."
