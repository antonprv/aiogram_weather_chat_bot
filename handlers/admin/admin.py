from typing import Any

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hitalic, hbold
from aiogram.utils.keyboard import InlineKeyboardBuilder, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardMarkup

from database import orm
import keyboards as kb
from keyboards import ButtonCallback
from loader import dp
from states import ChoiceCityWeather, SetUserCity
from loader import bot
from settings.bot_config import TG_BOT_ADMINS




@dp.message(kb.check_text_filter(kb.administrator))
async def process_admin_panel(message: Message):
    btn1 = KeyboardButton(text=user_list)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = 'Админ-панель'
    await message.answer(text=text, reply_markup=markup)


@dp.message(kb.check_text_filter(kb.user_list))
async def process_get_all_users(message: Message):
