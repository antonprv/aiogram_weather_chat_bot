import json

import requests

from settings.api_config import *


def main():
    get_weather('Калининград')


def get_city_coord(city):
    payload = {'apikey': GEO_KEY, 'geocode': city, 'format': 'json'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo = json.loads(r.text)
    return (geo['response']['GeoObjectCollection']['featureMember'][0]
    ['GeoObject']['Point']['pos'])


def get_weather(city):
    coordinates = get_city_coord(city).split()
    payload = {'lat': coordinates[1], 'lon': coordinates[0],
               'lang': 'ru_RU'}
    r = requests.get('https://api.weather.yandex.ru/v2/fact',
                     params=payload, headers=WEATHER_KEY)
    # Преобразуем полученный json файл в многоуровневый словарь
    weather_data = json.loads(r.text)
    return weather_data


if __name__ == '__main__':
    main()
