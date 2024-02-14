# "История"
from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hitalic, hbold

from database import orm
import keyboards as kb
from keyboards import ButtonCallback
from loader import dp
from states import ShowHistory
from settings.bot_config import HISTORY_ITEMS
from .user_dp import dp, process_show_menu
from loader import bot


msg1: str = 'Вы перешли в раздел истории'
msg2: str = '<b>Все ваши запросы:</b>'

@dp.message(F.text == kb.weather_history)
async def process_get_reports(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    reports = orm.get_reports(tg_id=tg_id)
    await state.set_state(ShowHistory.history_viewing)
    await state.update_data(reports=reports, start_index=0, curr_page=1)
    data = await state.get_data()
    markup = kb.history_page_markup(reports=data.get('reports'))
    await message.answer(text=msg1,
                         reply_markup=kb.history_delete_all(tg_id=tg_id))
    await message.answer(text=msg2,
                         reply_markup=markup)


@dp.callback_query(ShowHistory.history_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'next'))
async def process_history_next(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    reports = data.get('reports')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    start_index += HISTORY_ITEMS
    curr_page += 1
    await state.update_data(start_index=start_index, curr_page=curr_page)

    markup = kb.history_page_markup(reports=reports, start_index=start_index,
                                    curr_page=curr_page)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(ShowHistory.history_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'back'))
async def process_history_back(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    reports = data.get('reports')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    start_index -= HISTORY_ITEMS
    curr_page -= 1
    await state.update_data(start_index=start_index, curr_page=curr_page)

    markup = kb.history_page_markup(reports=reports, start_index=start_index,
                                    curr_page=curr_page)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(ShowHistory.history_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'report'))
async def process_report_details(query: CallbackQuery, state: FSMContext,
                                 callback_data: ButtonCallback):
    report_id = callback_data.cb_id
    text = kb.history_report_text(report_id=report_id)
    data = await state.get_data()
    markup = kb.history_report_markup(report_id=report_id,
                                      curr_page_data=data.get('start_index'))

    await query.message.edit_text(text=text)
    await query.message.edit_reply_markup(reply_markup=markup)


# "Вернуться"
@dp.callback_query(ShowHistory.history_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'return'))
async def process_report_return(query: CallbackQuery, state: FSMContext,
                                callback_data: ButtonCallback):
    start_index = callback_data.cb_id
    await state.update_data(start_index=start_index)
    data = await state.get_data()
    reports = data.get('reports')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    markup = kb.history_page_markup(reports=reports, start_index=start_index,
                                    curr_page=curr_page)
    await query.message.edit_text(text=msg1)
    await query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(ShowHistory.history_viewing,
                   ButtonCallback.filter(F.cb_prefix == 'delete'))
async def process_delete_report(query: CallbackQuery,
                                state: FSMContext,
                                callback_data: ButtonCallback):
    report_id = callback_data.cb_id
    orm.delete_report(report_id)
    reports = orm.get_reports(query.from_user.id)
    await state.update_data(reports=reports)
    data = await state.get_data()
    reports = data.get('reports')
    start_index = data.get('start_index')
    curr_page = data.get('curr_page')
    markup = kb.history_page_markup(reports=reports, start_index=start_index,
                                    curr_page=curr_page)
    await query.answer(text='Отчёт удалён ✅')
    await query.message.edit_text(text=msg1)
    await query.message.edit_reply_markup(reply_markup=markup)

@dp.message(F.text == kb.delete_all_reps)
async def process_clear_history(message: Message):
    await message.answer(text=kb.are_you_sure,
                         reply_markup=kb.history_confirm_deletion())



@dp.message(ShowHistory.history_viewing, F.text == kb.weather_menu)
async def process_clean_on_menu(message: Message, state: FSMContext):
    await state.clear()
    await process_show_menu(message)
