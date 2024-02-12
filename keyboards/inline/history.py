from math import ceil

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold

from settings.bot_config import HISTORY_ITEMS
from database import orm
from loader import bot

next_btn = 'Вперёд ➡'
back_btn = 'Назад ⬅'


class ButtonCallback(CallbackData, prefix='btn'):
    cb_prefix: str
    cb_id: int


# Пагинация страниц истории.
def history_page_markup(reports: dict[str], start_index: int = 0,
                        curr_page: int = 1):
    builder = InlineKeyboardBuilder()
    total_pages: int = ceil(len(reports) / HISTORY_ITEMS)
    end_index = min(start_index + HISTORY_ITEMS, len(reports))

    for report in reports[start_index:end_index]:
        text = (f'{report.city} {report.date.day}.{report.date.month}'
                f'.{report.date.year}')
        history_cb = ButtonCallback(cb_prefix='report',
                                    cb_id=report.id)
        builder.button(text=text, callback_data=history_cb)

    builder.adjust(1)

    page_n_cb = ButtonCallback(cb_prefix='next', cb_id=start_index)

    btn1 = InlineKeyboardButton(text=f'{curr_page}/{total_pages}',
                                callback_data='None')

    btn2 = InlineKeyboardButton(text=next_btn,
                                callback_data=page_n_cb.pack())

    page_b_cb = ButtonCallback(cb_prefix='back', cb_id=start_index)
    btn3 = InlineKeyboardButton(text=back_btn,
                                callback_data=page_b_cb.pack())

    if curr_page == 1:
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


def history_report_text(report_id):
    report = orm.get_report_details(report_id=report_id)
    text = (f'Город: {hbold(report.city)},\n'
            f'Дата и время запроса: {report.date.day}.{report.date.month}'
            f'.{report.date.year} в {report.date.hour}:{report.date.minute},\n'
            f'Температура: {report.temp}°C,\n'
            f'Ощущалось как {report.feels_like}°C,\n'
            f'Скорость ветра {report.wind_speed}м/c,\n'
            f'Давление {report.pressure_mm}мм.')

    return text