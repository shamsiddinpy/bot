from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_phone():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Телефон рақамни юбориш", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def language_btn():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="uzbek", callback_data="uzbek_btn"),
                InlineKeyboardButton(text="узбек", callback_data="узбек_btn")
            ]
        ]
    )
