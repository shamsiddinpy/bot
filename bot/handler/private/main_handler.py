from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.handler.buttons.inline import language_btn, main_btn
from bot.handler.language.language import MESSAGES
from bot.handler.state.main_state import MainStatesGroup
from config.base import session
from config.model import TelegramUser

handler_start_router = Router()


@handler_start_router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    telegram_id = msg.from_user.id
    user_id = msg.from_user.username
    last_name = msg.from_user.last_name
    first_name = msg.from_user.first_name
    user_int_db = session.query(TelegramUser).filter(TelegramUser.telegram_id == telegram_id).first()

    if not user_int_db:
        new_user = TelegramUser(
            telegram_id=telegram_id,
            username=user_id,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(new_user)
        session.commit()

    await state.set_state(MainStatesGroup.select_language)
    await msg.answer("Tilni tanlang", reply_markup=language_btn())


@handler_start_router.message(lambda msg: msg.text in ('Uzbek', 'Uzbek(узбек)'), MainStatesGroup.select_language)
async def language_handler(msg: Message, state: FSMContext):
    lang = msg.text.split()[1]
    state_data = await state.get_data()
    state_data.update({"language": lang})
    await state.update_data(state_data)
    await msg.answer(MESSAGES[lang]['language_choose'], reply_markup=main_btn(lang))


@handler_start_router.message(lambda msg: msg.text == MESSAGES['Uzbek']['language_choose'])
@handler_start_router.message(lambda msg: msg.text == MESSAGES['Uz']['language_choose'])
async def language_choose_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await msg.answer(MainStatesGroup.select_language)
    await msg.answer(MESSAGES[lang][''], reply_markup=language_btn())


@handler_start_router.callback_query(lambda c: c.data in ['uzbek_btn', 'узбек_btn'])
async def start_callback_handler(c: CallbackQuery, state: FSMContext):
    language = 'Uzbek' if c.data == 'uzbek_btn' else 'Uz'
    telegram_id = c.from_user.id
    user = session.query(TelegramUser).filter(TelegramUser.telegram_id == telegram_id).first()
    if not user:
        user.language_code = language
        session.commit()
    await state.update_data(language=language)
    await state.set_state(MainStatesGroup.main_jshshir)
    await c.message.answer(MESSAGES[language]['enter_jshshir'])
    await c.answer()
