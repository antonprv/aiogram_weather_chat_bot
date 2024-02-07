from math import ceil

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, \
    InlineKeyboardMarkup, InlineKeyboardButton

from settings.bot_config import HISTORY_ITEMS

next_btn = 'Вперёд ➡'
prev_btn = 'Назад ⬅'


class ButtonCallback(CallbackData):
    cb_prefix: str
    cb_id: int


def history_page_markup(reports: dict[str]):
    builder = InlineKeyboardBuilder()
    curr_page: int = 1
    total_pages: int = ceil(len(reports) / HISTORY_ITEMS)

    for report in reports[:curr_page * HISTORY_ITEMS]:
        text = (f'{report.city} {report.date.day}.{report.date.month}'
                f'.{report.date.year}')
        history_cb = ButtonCallback(cb_prefix='report', cb_id=report.id)
        builder.button(text=text, callback_data=history_cb)
    builder.adjust(1)

    curr_page += 1
    page_cb = ButtonCallback(cb_prefix='next', cb_id=str(curr_page))

    btn1 = InlineKeyboardButton(text=f'{curr_page-1}/{total_pages}',
                                callback_data='None')
    btn2 = InlineKeyboardButton(text=next_btn, callback_data=page_cb.pack())

    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
    builder.attach(InlineKeyboardBuilder.from_markup(markup))

    return builder.as_markup()
