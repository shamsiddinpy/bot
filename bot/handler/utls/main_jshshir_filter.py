import re
from datetime import datetime


def is_jshshir_number_filter(number: str) -> bool:
    return bool(re.findall(r"\d{14}", number))


def format_phone_number(phone: str) -> str:
    digits = re.findall(r'\d+', phone)
    if len(digits) == 3:
        return f"({digits[0]})-{digits[1]}-{digits[2]}"
    return phone


def normalize_phone(phone: str) -> str:
    return ''.join(filter(str.isdigit, phone))


def format_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")
        return date_obj.strftime("%d.%m.%Y")
    except:
        return date_str
