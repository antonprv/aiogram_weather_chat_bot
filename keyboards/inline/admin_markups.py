from math import ceil

from aiogram.utils.keyboard import InlineKeyboardBuilder, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton

from database import orm
from ..callback_class import ButtonCallback
from settings.bot_config import TG_BOT_ADMINS, ADMIN_HISTORY_ITEMS

greet = 'Вы перешли в админ-панель'
user_list = 'Список пользователей:'
combined = greet + '\n' + user_list

administrator = 'Администратор'

next_btn = 'Вперёд ➡'
back_btn = 'Назад ⬅'

empty = 'Пока нет пользователей :('


def user_reports_text(usr_id):
    name = orm.get_user_data(usr_id).name
    return f'Все запросы пользователя {name}'


def check_text_filter(text: str):
    return (lambda message: message.from_user.id in TG_BOT_ADMINS
                            and message.text == text)


def users_page_markup(users: dict[str], start_index: int = 0,
                      curr_page: int = 1):
    builder = InlineKeyboardBuilder()
    total_pages: int = ceil(len(users) / ADMIN_HISTORY_ITEMS)
    end_index = min(start_index + ADMIN_HISTORY_ITEMS, len(users))

    for user in users[start_index:end_index]:
        if user.tg_id in TG_BOT_ADMINS:
            text = (f'{user.name} ({administrator})'
                    f' {user.connection_date.day}.'
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


def admin_user_markup(usr_id, curr_page_data):
    tg_id = orm.get_user_tg_id(usr_id=usr_id)
    back_btn_cb = ButtonCallback(cb_prefix='return', cb_id=curr_page_data)
    details_btn_cb = ButtonCallback(cb_prefix='details', cb_id=tg_id)
    btn1 = InlineKeyboardButton(text='Вернуться',
                                callback_data=back_btn_cb.pack())
    btn2 = InlineKeyboardButton(text='Посмотреть запросы',
                                callback_data=details_btn_cb.pack())
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return markup


def admin_report_details_markup(curr_page_data):
    back_btn_cb = ButtonCallback(cb_prefix='b_return', cb_id=curr_page_data)
    btn1 = InlineKeyboardButton(text='Вернуться',
                                callback_data=back_btn_cb.pack())
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return markup


def admin_user_text(usr_id):
    user = orm.get_user_data(usr_id)
    text = (f'Имя пользователя: {user.name},'
            f'\nГород пользователя: {user.city},'
            f'\nДата подключения: '
            f'{user.connection_date.day}.'
            f'{user.connection_date.month}.'
            f'{user.connection_date.year}, '
            f'\nЛокальное время подключения: '
            f'{user.connection_date.hour}:'
            f'{user.connection_date.minute}')

    return text


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
    btn4 = InlineKeyboardButton(text=empty,
                                callback_data='None')
    btn5 =

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