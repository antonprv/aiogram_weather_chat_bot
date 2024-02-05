from aiogram.utils.markdown import hitalic, hbold

from api_requests import request

weather_my_city = 'Погода в моём городе'
weather_other_place = 'Погода в другом месте'
weather_history = 'История'
weather_set_city = 'Установить свой город'
weather_menu = 'Меню'
wip_message = 'Я пока так не умею 😔'
city_is_lower = 'Названия городов пишутся с большой буквы!😡'


def show_weather(city):
    data = request.get_weather(city)
    return (f'Погода в <b>{hitalic(city)}</b>'
            f'\nТемпература: {hbold(data["temp"])}°C'
            f'\nОщущается как: {hbold(data["feels_like"])}°C'
            f'\nСкорость ветра: {hbold(data["wind_speed"])}м/c'
            f'\nДавление: {hbold(data["pressure_mm"])}мм')
