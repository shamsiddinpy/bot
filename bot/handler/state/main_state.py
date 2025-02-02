from aiogram.fsm.state import StatesGroup, State


class MainStatesGroup(StatesGroup):
    select_language = State()
    main_jshshir = State()
    main_phone = State()
    main_verify_code = State()
