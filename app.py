import asyncio
import logging
import sys
from typing import Any

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandObject, CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold, hitalic, hunderline, hblockquote
from aiogram.fsm.context import FSMContext

from settings import bot_config
from states.states import ChoiceCityWeather, SetUserCity
from keyboards.default.menu import *
from api_requests import request
from database import orm

bot = Bot(token=bot_config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start_message(message: Message):
    orm.add_user(tg_id=message.from_user.id,
                 name=message.from_user.first_name)
    text = (f'Привет, {hbold(message.from_user.first_name)}! Я бот,'
            f' который расскажет тебе о погоде на сегодня!')
    await message.answer(text=text)
    await show_menu(message)


@dp.message(F.text == weather_menu)
async def show_menu(message: Message):
    await message.delete()
    btn1 = KeyboardButton(text=weather_my_city)
    btn2 = KeyboardButton(text=weather_other_place)
    btn3 = KeyboardButton(text=weather_history)
    btn4 = KeyboardButton(text=weather_set_city)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4]],
                                 resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text='Меню:', reply_markup=markup)


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
    data = request.get_weather(city.get('waiting_city'))
    text = (f'Погода в <b>{hitalic(city.get("waiting_city"))}</b>'
            f'\nТемпература: {data["temp"]}°C'
            f'\nСкорость ветра: {data["wind_speed"]}м/c'
            f'\nДавление: {data["pressure_mm"]}мм')
    await message.answer(text=text)
    await show_menu(message)
    await state.clear()


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
    await show_menu
    await message.answer(text=text)
    await state.clear()


# Обработчик исключений
@dp.message(F.text)
async def no_such_function(message: Message):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    await message.answer(text=wip_message, reply_markup=markup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
