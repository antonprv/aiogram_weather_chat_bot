import asyncio
import logging
import sys

from aiogram import F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database import orm
import handlers
from keyboards.default.menu import *
from loader import bot, dp


async def main():
    await dp.start_polling(bot)


@dp.message(F.text)
async def no_such_function(message: Message):
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    await message.answer(text=wip_message, reply_markup=markup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
