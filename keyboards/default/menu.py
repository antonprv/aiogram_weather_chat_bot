from aiogram.utils.markdown import hitalic, hbold
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from api_requests import request

weather_my_city = 'Погода в моём городе'
weather_other_place = 'Погода в другом месте'
weather_history = 'История'
weather_set_city = 'Установить свой город'
weather_menu = 'Меню'
wip_message = 'Я пока так не умею 😔'
city_is_lower = 'Названия городов пишутся с большой буквы!😡'


def main_menu_markup():
    btn1 = KeyboardButton(text=weather_my_city)
    btn2 = KeyboardButton(text=weather_other_place)
    btn3 = KeyboardButton(text=weather_history)
    btn4 = KeyboardButton(text=weather_set_city)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4]],
                                 resize_keyboard=True, one_time_keyboard=True)
    return markup


def back_to_menu_markup():
    btn1 = KeyboardButton(text=weather_menu)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    return markup


def show_weather(city):
    data = request.get_weather(city)
    return (f'Погода в <b>{hitalic(city)} '
            f'(распознано как {hbold(data["location"]["name"])})</b>'
            f'\nТемпература: '
            f'{hbold(data["current"]["temp_c"])}°C'
            f'\nОщущается как: '
            f'{hbold(data["current"]["feelslike_c"])}°C'
            f'\nСкорость ветра: '
            f'{hbold(data["current"]["wind_kph"])}м/c'
            f'\nДавление: '
            f'{hbold(round((data["current"]["pressure_mb"] * 0.750062), 2))}мм')
