import json

import requests

from ..settings import config


def main():
    get_city_coord('Калининград')

def get_city_coord(city):
    payload = {'geocode' : city, 'apikey' : config.GEO_KEY, 'format' : 'json'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo = json.loads(r.text)
    return (geo['response']['GeoObjectCollection']['featureMember'][0]
                 ['GeoObject']['Point']['pos'])


def get_weather(city):
    coordinates = get_city_coord(city).split()
    payload = {'lat' : coordinates[1], 'lon' : coordinates[0],
               'lang' : 'ru_RU'}
    r = requests.get('https://api_weather.yandex.ru/v2/forecast',
                     params=payload, headers=config.weather_key)
    weather_data = json.loads(r.text)
    return weather_data





if __name__ == '__main__':
    main()