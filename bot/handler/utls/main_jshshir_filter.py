import re


def is_jshshir_number_filter(number: str) -> bool:
    """JShShIR 14 xonali va faqat raqamlardan iborat ekanligini tekshiradi."""
    return bool(re.findall(r"\d{14}", number))


def format_phone_number(phone: str) -> str:
    digits = re.findall(r'\d+', phone)
    if len(digits) == 3:
        return f"({digits[0]})-{digits[1]}-{digits[2]}"
    return phone
