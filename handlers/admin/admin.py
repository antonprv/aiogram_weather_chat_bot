from aiogram.types import Message
from aiogram.utils.keyboard import KeyboardButton, \
    ReplyKeyboardMarkup

import keyboards as kb
from loader import dp


@dp.message(kb.check_text_filter(kb.administrator))
async def process_admin_panel(message: Message):
    btn1 = KeyboardButton(text=user_list)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = 'Админ-панель'
    await message.answer(text=text, reply_markup=markup)


@dp.message(kb.check_text_filter(kb.user_list))
async def process_get_all_users(message: Message):
