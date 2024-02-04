from typing import Any

from aiogram import Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from states.states import ChoiceCityWeather, SetUserCity
from keyboards.default.menu import *
from database import orm
from app import show_menu

dp = Dispatcher()
router = Router()
dp.include_router(router)


# "Погода в другом месте"
@dp.message(F.text == weather_other_place)
async def city_start(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    text = 'Введите название города'
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(ChoiceCityWeather.waiting_city)


@dp.message(ChoiceCityWeather.waiting_city)
async def city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=city_is_lower)
        return
    # Записываем в данные статуса город, и сразу достаём.
    # Хранится всё в оперативной памяти.
    await state.update_data(waiting_city=message.text)
    city: dict[str, Any] = await state.get_data()
    # Так как city - словарь, получаем значение по ключу
    # через метод .get
    text = show_weather(city.get('waiting_city'))
    await message.answer(text=text)
    await show_menu(message)
    await state.clear()


# "Установить свой город"
@dp.message(F.text == weather_set_city)
async def set_user_city_start(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    text = 'В каком городе проживаете?'
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(SetUserCity.waiting_user_city)


@dp.message(SetUserCity.waiting_user_city)
async def user_city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=city_is_lower)
        return
    await state.update_data(cust_user_city=message.text)
    user_data = await state.get_data()
    orm.set_user_city(message.from_user.id, user_data.get('cust_user_city'))
    text = (f'Запомнил! Ваш город - '
            f'<b>{hitalic(user_data.get("cust_user_city"))}</b>,'
            f' {hbold(message.from_user.first_name)}!')
    await message.answer(text=text)
    await show_menu(message)
    await state.clear()


# "Погода в моём городе"
@dp.message(F.text == weather_my_city)
async def show_my_weather(message: Message):
    city = orm.get_user_city(tg_id=message.from_user.id)
    if city is None:
        text = 'Пожалуйста, установите город проживания.'
        await message.answer(text=text)
        await show_menu(message)
    else:
        text = show_weather(city)
        await show_menu(message)
        await message.answer(text=text)
