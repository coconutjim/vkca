__author__ = 'Lev'

import requests
import json

from settings import WEATHER_KEY


API_URL = 'http://api.wunderground.com/api/' + WEATHER_KEY


# consider errors sometimes
def default_weather():
    response = requests.get(API_URL + '/forecast/lang:RU/q/Russia/Moscow.json')
    result = json.loads(response.text)['forecast']['txt_forecast']
    res = ''
    for period in result['forecastday']:
        res += period['title'] + '\n'
        res += period['fcttext_metric'] + '\n\n'
    return res[:-2]
