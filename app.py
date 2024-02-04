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
from handlers import dp

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


# Обработчик кнопки меню.
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



# Обработчик исключений
@dp.message(F.text)
async def no_such_function(message: Message):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    await message.answer(text=wip_message, reply_markup=markup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
