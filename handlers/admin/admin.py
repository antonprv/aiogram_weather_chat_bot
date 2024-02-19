from aiogram.types import Message

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import AdminPanel
from database import orm
import keyboards as kb
from loader import dp
from handlers.user.user_dp import process_show_menu
from settings.bot_config import ADMIN_HISTORY_ITEMS
from keyboards import ButtonCallback


@dp.message(kb.check_text_filter(kb.administrator))
async def process_admin_panel(message: Message, state: FSMContext):
    users = orm.get_all_users()
    await state.set_state(AdminPanel.panel_viewing)
    await state.update_data(users=users, start_index=0, curr_page=1)
    data = await state.get_data()
    markup = kb.users_page_markup(users=data.get('users'))
    await process_show_menu(message=message)
    await message.answer(text=kb.combined,
                         reply_markup=markup)


@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'next'))
@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'back'))
async def process_history_buttons(query: CallbackQuery, state: FSMContext,
                                  callback_data: ButtonCallback):
    data = await state.get_data()
    users = data.get('users')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')

    if callback_data.cb_prefix == 'next':
        start_index += ADMIN_HISTORY_ITEMS
        curr_page += 1
        await state.update_data(start_index=start_index, curr_page=curr_page)

        markup = kb.users_page_markup(users=users, start_index=start_index,
                                      curr_page=curr_page)
        await query.message.edit_reply_markup(reply_markup=markup)
    elif callback_data.cb_prefix == 'back':
        start_index -= ADMIN_HISTORY_ITEMS
        curr_page -= 1
        await state.update_data(start_index=start_index, curr_page=curr_page)

        markup = kb.users_page_markup(users=users, start_index=start_index,
                                      curr_page=curr_page)
        await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'user'))
async def process_report_details(query: CallbackQuery, state: FSMContext,
                                 callback_data: ButtonCallback):
    usr_id = callback_data.cb_id
    text = kb.admin_user_text(usr_id=usr_id)
    data = await state.get_data()
    markup = kb.admin_user_details_markup(
        curr_page_data=data.get('start_index'))

    await query.message.edit_text(text=text)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'return'))
async def process_report_return(query: CallbackQuery, state: FSMContext,
                                callback_data: ButtonCallback):
    start_index = callback_data.cb_id
    await state.update_data(start_index=start_index)
    data = await state.get_data()
    users = data.get('users')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    markup = kb.users_page_markup(users=users, start_index=start_index,
                                  curr_page=curr_page)
    await query.message.edit_text(text=kb.combined)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(AdminPanel.panel_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'details'))
def show_user_reports(query: CallbackQuery, state: FSMContext,
                      callback_data: ButtonCallback):

