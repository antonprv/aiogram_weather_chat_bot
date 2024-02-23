from aiogram.types import Message

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import AdminPanel, ShowHistory
from database import orm
import keyboards as kb
from loader import dp
from handlers.user.user_dp import process_show_menu
from settings.bot_config import ADMIN_USERS_ITEMS, HISTORY_ITEMS
from keyboards import ButtonCallback


# Список пользователей.
@dp.message(kb.check_text_filter(kb.text_administrator))
async def process_admin_panel(message: Message, state: FSMContext):
    users = orm.get_all_users()
    await state.set_state(AdminPanel.panel_viewing)
    await state.update_data(users=users, adm_start_index=0, adm_curr_page=1)
    data = await state.get_data()
    markup = kb.users_page_markup(users=data.get('users'))
    await process_show_menu(message=message)
    await message.answer(text=kb.text_combined,
                         reply_markup=markup)


# Кнопки "вперёд" и "назад" в списке пользователей.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'next'))
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'back'))
async def process_users_buttons(query: CallbackQuery, state: FSMContext,
                                callback_data: ButtonCallback):
    data = await state.get_data()
    users = data.get('users')
    start_index = data.get('adm_start_index')
    curr_page = data.get('adm_curr_page')

    if callback_data.cb_prefix == 'next':
        start_index += ADMIN_USERS_ITEMS
        curr_page += 1
        await state.update_data(adm_start_index=start_index, adm_curr_page=curr_page)

        markup = kb.users_page_markup(users=users, start_index=start_index,
                                      curr_page=curr_page)
        await query.message.edit_reply_markup(reply_markup=markup)
    elif callback_data.cb_prefix == 'back':
        start_index -= ADMIN_USERS_ITEMS
        curr_page -= 1
        await state.update_data(adm_start_index=start_index,
                                adm_curr_page=curr_page)

        markup = kb.users_page_markup(users=users, start_index=start_index,
                                      curr_page=curr_page)
        await query.message.edit_reply_markup(reply_markup=markup)


# Детально о пользователе.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'user'))
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'h_turn_back'))
async def process_report_details(query: CallbackQuery, state: FSMContext,
                                 callback_data: ButtonCallback):
    usr_id = callback_data.cb_id
    await state.update_data(usr_id=usr_id)
    text = kb.admin_user_text(usr_id=usr_id)
    data = await state.get_data()
    markup = kb.admin_user_markup(usr_id=usr_id,
                                  curr_page_data=data.get('adm_start_index'))

    await query.message.edit_text(text=text)
    await query.message.edit_reply_markup(reply_markup=markup)


# Вернуться к просмотру пользователей.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'return'))
async def process_report_return(query: CallbackQuery, state: FSMContext,
                                callback_data: ButtonCallback):
    start_index = callback_data.cb_id
    await state.update_data(adm_start_index=start_index)
    data = await state.get_data()
    users = data.get('users')
    start_index = data.get('adm_start_index')
    curr_page = data.get('adm_curr_page')
    markup = kb.users_page_markup(users=users, start_index=start_index,
                                  curr_page=curr_page)
    await query.message.edit_text(text=kb.text_combined)
    await query.message.edit_reply_markup(reply_markup=markup)


# Список запросов пользователя.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'details'))
async def show_user_reports(query: CallbackQuery, state: FSMContext,
                            callback_data: ButtonCallback):
    tg_id = callback_data.cb_id
    await query.message.delete()
    reports = orm.get_reports(tg_id=tg_id)
    await state.update_data(reports=reports, start_index=0, curr_page=1)
    data = await state.get_data()
    markup = kb.adm_history_page_markup(reports=data.get('reports'))
    await query.message.answer(text=kb.user_reports_text(
        usr_id=data.get('usr_id')),
        reply_markup=markup)


# Посмотреть детали запроса пользователя.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'report'))
async def process_report_details(query: CallbackQuery, state: FSMContext,
                                 callback_data: ButtonCallback):
    report_id = callback_data.cb_id
    text = kb.history_report_text(report_id=report_id)
    data = await state.get_data()
    markup = kb.admin_report_details_markup(
        curr_page_data=data.get('start_index'))

    await query.message.edit_text(text=text)
    await query.message.edit_reply_markup(reply_markup=markup)


# Вернуться с деталей назад к списку.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'b_return'))
async def process_adm_report_return(query: CallbackQuery, state: FSMContext,
                                    callback_data: ButtonCallback):
    start_index = callback_data.cb_id
    await state.update_data(start_index=start_index)
    data = await state.get_data()
    reports = data.get('reports')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    usr_id = data.get('usr_id')
    markup = kb.adm_history_page_markup(reports=reports,
                                        start_index=start_index,
                                        curr_page=curr_page)
    await query.message.edit_text(text=kb.user_reports_text(usr_id))
    await query.message.edit_reply_markup(reply_markup=markup)


# Обработчик двух кнопок в списке запросов.
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'h_next'))
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'h_back'))
async def process_users_buttons(query: CallbackQuery, state: FSMContext,
                                callback_data: ButtonCallback):
    data = await state.get_data()
    reports = data.get('reports')
    usr_id = data.get('usr_id')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')

    if callback_data.cb_prefix == 'h_next':
        start_index += HISTORY_ITEMS
        curr_page += 1
        await state.update_data(start_index=start_index,
                                curr_page=curr_page)

        markup = kb.adm_history_page_markup(reports=reports,
                                            start_index=start_index,
                                            curr_page=curr_page,
                                            usr_id=usr_id)
        await query.message.edit_reply_markup(reply_markup=markup)
    elif callback_data.cb_prefix == 'h_back':
        start_index -= HISTORY_ITEMS
        curr_page -= 1
        await state.update_data(start_index=start_index,
                                curr_page=curr_page)

        markup = kb.adm_history_page_markup(reports=reports,
                                            start_index=start_index,
                                            curr_page=curr_page,
                                            usr_id=usr_id)
        await query.message.edit_reply_markup(reply_markup=markup)


