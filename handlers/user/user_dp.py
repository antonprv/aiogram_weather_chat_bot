from typing import Any

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hitalic, hbold

from database import orm
import keyboards as kb
from keyboards import ButtonCallback
from loader import dp
from states import ChoiceCityWeather, SetUserCity, ShowHistory
from settings.bot_config import HISTORY_ITEMS


# "/start"
@dp.message(CommandStart())
async def process_start_message(message: Message):
    orm.add_user(tg_id=message.from_user.id,
                 name=message.from_user.first_name)
    text = (f'Привет, {hbold(message.from_user.first_name)}! Я бот,'
            f' который расскажет тебе о погоде на сегодня!')
    await message.answer(text=text)
    await process_show_menu(message)


# Обработчик кнопки меню.
@dp.message(F.text == kb.weather_menu)
async def process_show_menu(message: Message):
    await message.answer(text='Меню:', reply_markup=kb.main_menu_markup())


# "Погода в другом месте"
@dp.message(F.text == kb.weather_other_place)
async def process_city_start(message: Message, state: FSMContext):
    text = 'Введите название города'
    await message.answer(text=text, reply_markup=kb.back_to_menu_markup())
    await state.set_state(ChoiceCityWeather.waiting_city)


@dp.message(ChoiceCityWeather.waiting_city)
async def process_city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=kb.city_is_lower)
        return
    # Записываем в данные статуса город, и сразу достаём.
    # Хранится всё в оперативной памяти.
    await state.update_data(waiting_city=message.text)
    city: dict[str, Any] = await state.get_data()
    # Так как city - словарь, получаем значение по ключу
    # через метод .get
    text = kb.show_weather(city.get('waiting_city'))
    # Пишем в бд отчёт о погоде.
    orm.save_report(tg_id=message.from_user.id, city=message.text)
    await message.answer(text=text)
    await process_show_menu(message)
    await state.clear()


# "Установить свой город"
@dp.message(F.text == kb.weather_set_city)
async def process_set_user_city_start(message: Message, state: FSMContext):
    text = 'В каком городе проживаете?'
    await message.answer(text=text, reply_markup=kb.back_to_menu_markup())
    await state.set_state(SetUserCity.waiting_user_city)


@dp.message(SetUserCity.waiting_user_city)
async def process_user_city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=kb.city_is_lower)
        return
    await state.update_data(cust_user_city=message.text)
    user_data = await state.get_data()
    orm.set_user_city(message.from_user.id, user_data.get('cust_user_city'))
    text = (f'Запомнил! Ваш город - '
            f'<b>{hitalic(user_data.get("cust_user_city"))}</b>,'
            f' {hbold(message.from_user.first_name)}!')
    await message.answer(text=text)
    await process_show_menu(message)
    await state.clear()


# "Погода в моём городе"
@dp.message(F.text == kb.weather_my_city)
async def process_show_my_weather(message: Message):
    city = orm.get_user_city(tg_id=message.from_user.id)
    if city is None:
        text = 'Сначала вам нужно <b>установить свой город</b>.'
        await message.answer(text=text)
        await process_show_menu(message)
    else:
        text = kb.show_weather(city=city)
        orm.save_report(tg_id=message.from_user.id)
        await process_show_menu(message)
        await message.answer(text=text)


# "История"
msg1: str = 'Вы перешли в раздел истории'
msg2: str = '<b>Все ваши запросы:</b>'

@dp.message(F.text == kb.weather_history)
async def process_get_reports(message: Message, state: FSMContext):
    reports = orm.get_reports(message.from_user.id)
    await state.set_state(ShowHistory.history_viewing)
    await state.update_data(reports=reports, start_index=0, curr_page=1)
    data = await state.get_data()
    markup = kb.history_page_markup(reports=data.get('reports'))
    await message.answer(text=msg1,
                         reply_markup=kb.back_to_menu_markup())
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


@dp.message(ShowHistory.history_viewing, F.text == kb.weather_menu)
async def process_clean_on_menu(message: Message, state: FSMContext):
    await state.clear()
    await process_show_menu(message)


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
async def process_delete_report(query: CallbackQuery, message: Message,
                                state: FSMContext,
                                callback_data: ButtonCallback):
    orm.