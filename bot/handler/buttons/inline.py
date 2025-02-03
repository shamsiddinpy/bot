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


def main_btn(lang: Optional[str] = 'uzbek') -> ReplyKeyboardMarkup:
    if lang is None or lang not in MESSAGES:
        lang = 'uzbek'

    text_btn = MESSAGES[lang]
    print(text_btn)
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text_btn['computer_literacy'])],  # Removed request_contact
            [KeyboardButton(text=text_btn['sample_of_tests']),
             KeyboardButton(text=text_btn['profile_user'])],
            [KeyboardButton(text=text_btn['back'])],
        ],
        resize_keyboard=True
    )
