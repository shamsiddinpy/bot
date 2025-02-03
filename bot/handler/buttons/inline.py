from typing import Optional

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.handler.language.language import MESSAGES


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
                InlineKeyboardButton(text="Uzbek", callback_data="uzbek_btn"),
                InlineKeyboardButton(text="Uzbek(узбек)", callback_data="узбек_btn")
            ]
        ]
    )


def main_btn1(lang: Optional[str] = 'Uzbek') -> ReplyKeyboardMarkup:
    lang = lang if lang in MESSAGES else 'Uzbek'
    text_btn = MESSAGES[lang]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text_btn['computer_literacy'])],
            [KeyboardButton(text=text_btn['sample_of_tests']), KeyboardButton(text=text_btn['profile_user'])],
            [KeyboardButton(text=text_btn['back']), KeyboardButton(text=text_btn['language_choose'])],
        ],
        resize_keyboard=True
    )
