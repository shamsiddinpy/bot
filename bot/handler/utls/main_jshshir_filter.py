import re


def is_jshshir_number_filter(number: str) -> bool:
    """JShShIR 14 xonali va faqat raqamlardan iborat ekanligini tekshiradi."""
    return bool(re.findall(r"\d{14}", number))
