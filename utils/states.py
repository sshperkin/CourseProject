from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    country = State()
    dates = State()
    people_num = State()
    city = State()
