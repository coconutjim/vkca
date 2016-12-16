# coding: utf8
__author__ = 'Lev'

import requests
import json

from settings import WEATHER_KEY


API_URL = 'http://api.wunderground.com/api/' + WEATHER_KEY

weather_locale_dict = dict(ru='RU', eng='ENG')
wind_label_dict = dict(ru=u'Ветер', eng='Wind')
wind_spd_dict = dict(ru=u'км/ч', eng='km/h')


def default_weather(locale='ru'):
    response = requests.get(API_URL + '/forecast/lang:{}/q/Russia/Moscow.json'.format(weather_locale_dict[locale]))
    result = json.loads(response.text)['forecast']['txt_forecast']
    res = ''
    for period in result['forecastday']:
        res += period['title'] + '\n'
        res += period['fcttext_metric'] + '\n\n'
    return res[:-2]


def hourly_weather(locale='ru'):
    response = requests.get(API_URL + '/hourly/lang:{}/q/Russia/Moscow.json'.format(weather_locale_dict[locale]))
    result = json.loads(response.text)['hourly_forecast']
    res = ''
    for period in result:
        time = period['FCTTIME']
        res += '{} {}:{} - '.format(time['weekday_name'], time['hour'], time['min'])
        res += '{}. {}C.'.format(period['condition'], period['temp']['metric'], )
        if period['wspd']['metric'] != '0':
            res += ' {} {} {} {}'.format(wind_label_dict[locale], period['wdir']['dir'],
                                         period['wspd']['metric'], wind_spd_dict[locale])
        res += '\n'

    return res[:-1]

