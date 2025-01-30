from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_phone():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Телефон рақамни юбориш", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
