import re
from datetime import datetime


def is_jshshir_number_filter(number: str) -> bool:
    return bool(re.fullmatch(r"\d{14}", number))


def format_phone_number(phone: str) -> str:
    """Telefon raqamlarini (93)-908-12-17 formatiga o'tkazish"""
    digits = re.findall(r'\d+', phone)
    digits = ''.join(digits)  # Ro‘yxatni stringga aylantiramiz

    if len(digits) == 9:  # Masalan: 908121217
        return f"(9{digits[0]})-{digits[1:4]}-{digits[4:6]}-{digits[6:]}"
    elif len(digits) == 12 and digits.startswith("998"):  # Masalan: 998908121217
        return f"({digits[3:5]})-{digits[5:8]}-{digits[8:10]}-{digits[10:]}"

    return phone  # Agar formatga to‘g‘ri kelmasa, hech qanday o‘zgarish qilinmaydi


def normalize_phone(phone: str) -> str:
    """Faqat oxirgi 9 ta raqamni olish va keyin formatlash"""
    digits = ''.join(filter(str.isdigit, phone))[-9:]  # So‘nggi 9 ta raqamni olish
    return format_phone_number(digits)  # Formatga moslashtirish


def format_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return date_str
