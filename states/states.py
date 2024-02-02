from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class ChoiceCityWeather(StatesGroup):
    waiting_city = State()


class SetUserCity(StatesGroup):
    waiting_user_city = State()