from typing import Any
from math import ceil

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
from settings.bot_config import TG_BOT_ADMINS, ADMIN_HISTORY_ITEMS

administrator = 'Администратор'
user_list = 'Список пользователей'

next_btn = 'Вперёд ➡'
back_btn = 'Назад ⬅'

empty = 'Пока нет пользователей :('

def check_text_filter(text: str):
    return (lambda message: message.from_user.id in TG_BOT_ADMINS
                            and message.txt == text)


def users_page_markup(users: dict[str], start_index: int = 0,
                      curr_page: int = 1):
    builder = InlineKeyboardBuilder()
    total_pages: int = ceil(len(users) / ADMIN_HISTORY_ITEMS)
    end_index = min(start_index + ADMIN_HISTORY_ITEMS, len(users))

    for user in users[start_index:end_index]:
        if user.id in TG_BOT_ADMINS:
            text = (f'{user.name} (Администратор) {user.connection_date.day}.'
                    f'{user.connection_date.month}'
                    f'.{user.connection_date.year}')
        else:
            text = (f'{user.name} {user.connection_date.day}.'
                    f'{user.connection_date.month}'
                    f'.{user.connection_date.year}')
        user_cb = ButtonCallback(cb_prefix='user',
                                 cb_id=user.id)
        builder.button(text=text, callback_data=user_cb)

    builder.adjust(1)

    page_n_cb = ButtonCallback(cb_prefix='next', cb_id=start_index)

    btn1 = InlineKeyboardButton(text=f'{curr_page}/{total_pages}',
                                callback_data='None')

    btn2 = InlineKeyboardButton(text=next_btn,
                                callback_data=page_n_cb.pack())

    page_b_cb = ButtonCallback(cb_prefix='back', cb_id=start_index)
    btn3 = InlineKeyboardButton(text=back_btn,
                                callback_data=page_b_cb.pack())
    btn4 = InlineKeyboardButton(text=empty,
                                callback_data='None')

    if total_pages == 0:
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn4]])
    elif total_pages == 1:
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    elif curr_page == 1:
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
    elif curr_page == total_pages:
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn3, btn1]])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn3, btn1, btn2]])

    builder.attach(InlineKeyboardBuilder.from_markup(markup))

    return builder.as_markup()


def history_report_markup(report_id, curr_page_data):
    back_btn_cb = ButtonCallback(cb_prefix='return', cb_id=curr_page_data)
    delete_btn_cb = ButtonCallback(cb_prefix='delete', cb_id=report_id)
    btn1 = InlineKeyboardButton(text='Вернуться',
                                callback_data=back_btn_cb.pack())
    btn2 = InlineKeyboardButton(text='Удалить',
                                callback_data=delete_btn_cb.pack())

    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
    return markup
