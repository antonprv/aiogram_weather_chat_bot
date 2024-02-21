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
    payload = {'key': WEATHER_KEY, 'q': f'{coordinates[1]},{coordinates[0]}',
               'lang': 'ru'}
    r = requests.get('http://api.weatherapi.com/v1/current.json',
                     params=payload)
    # Преобразуем полученный json файл в многоуровневый словарь
    weather_data = json.loads(r.text)
    return weather_data['current']


if __name__ == '__main__':
    main()
