# coding: utf8
__author__ = 'Lev'

import requests
import json

from settings import WEATHER_KEY


API_URL = 'http://api.wunderground.com/api/' + WEATHER_KEY

weather_locale_dict = dict(ru='RU', eng='ENG')


# consider errors sometimes
def default_weather(locale):
    response = requests.get(API_URL + '/forecast/lang:{}/q/Russia/Moscow.json'.format(weather_locale_dict[locale]))
    result = json.loads(response.text)['forecast']['txt_forecast']
    res = ''
    for period in result['forecastday']:
        res += period['title'] + '\n'
        res += period['fcttext_metric'] + '\n\n'
    return res[:-2]
