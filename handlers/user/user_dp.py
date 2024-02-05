from typing import Any
from math import ceil

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from database import orm
from keyboards.default.menu import *
from states import ChoiceCityWeather, SetUserCity
from loader import dp


# "/start"
@dp.message(CommandStart())
async def process_start_message(message: Message):
    orm.add_user(tg_id=message.from_user.id,
                 name=message.from_user.first_name)
    text = (f'Привет, {hbold(message.from_user.first_name)}! Я бот,'
            f' который расскажет тебе о погоде на сегодня!')
    await message.answer(text=text)
    await process_show_menu(message)


# Обработчик кнопки меню.
@dp.message(F.text == weather_menu)
async def process_show_menu(message: Message):
    # await message.delete()
    btn1 = KeyboardButton(text=weather_my_city)
    btn2 = KeyboardButton(text=weather_other_place)
    btn3 = KeyboardButton(text=weather_history)
    btn4 = KeyboardButton(text=weather_set_city)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4]],
                                 resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text='Меню:', reply_markup=markup)


# "Погода в другом месте"
@dp.message(F.text == weather_other_place)
async def process_city_start(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    text = 'Введите название города'
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(ChoiceCityWeather.waiting_city)


@dp.message(ChoiceCityWeather.waiting_city)
async def process_city_chosen(message: Message, state: FSMContext):
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
    # Пишем в бд отчёт о погоде.
    orm.save_report(tg_id=message.from_user.id, city=message.text)
    await message.answer(text=text)
    await process_show_menu(message)
    await state.clear()


# "Установить свой город"
@dp.message(F.text == weather_set_city)
async def process_set_user_city_start(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    text = 'В каком городе проживаете?'
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(SetUserCity.waiting_user_city)


@dp.message(SetUserCity.waiting_user_city)
async def process_user_city_chosen(message: Message, state: FSMContext):
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
    await process_show_menu(message)
    await state.clear()


# "Погода в моём городе"
@dp.message(F.text == weather_my_city)
async def process_show_my_weather(message: Message):
    city = orm.get_user_city(tg_id=message.from_user.id)
    if city is None:
        text = 'Пожалуйста, установите город проживания.'
        await message.answer(text=text)
        await process_show_menu(message)
    else:
        text = show_weather(city)
        orm.save_report(tg_id=message.from_user.id)
        await process_show_menu(message)
        await message.answer(text=text)


# "История"
@dp.message(F.text == weather_history)
async def process_get_reports(message: Message):
    ...
