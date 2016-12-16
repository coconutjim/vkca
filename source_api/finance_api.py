# coding: utf8
__author__ = 'Lev'

import requests
import json

from settings import FINANCE_APP_ID
from api_utils import translate_text
from util import log

API_URL = 'https://openexchangerates.org/api/'


def get_currency_dictionaries():
    log('getting currencies dictionary...')
    method_url = API_URL + 'currencies.json'
    params = dict(app_id=FINANCE_APP_ID)
    response = requests.get(method_url, params=params)
    eng_dictionary = json.loads(response.text)
    log('got currencies dictionary...')
    to_tr = ''
    for v in eng_dictionary.values():
        to_tr += v + '\n'
    arr = translate_text(to_tr[:-1], lang='ru').split('\n')
    ru_dictionary = dict()
    i = 0
    for k in eng_dictionary.keys():
        ru_dictionary[k] = arr[i]
        i += 1
    return eng_dictionary, ru_dictionary


eng_dict, ru_dict = get_currency_dictionaries()

curr_locale_dict = dict(ru=ru_dict, eng=eng_dict)
label_locale_dict = dict(ru=u'Курсы валют по отношению к американскому доллару (USD):\n',
                         eng='Currencies based on USD:\n')

default_names = ['EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'XAU', 'ILS', 'RUB']


def get_currencies(names, locale='ru'):
    curr_dict = curr_locale_dict[locale]
    for name in names:
        if name not in curr_dict:
            return ''
    log('getting currencies...')
    method_url = API_URL + 'latest.json'
    params = dict(app_id=FINANCE_APP_ID)
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)['rates']
    res = label_locale_dict[locale]
    for name in names:
        res += '{} ({}) - {}\n'.format(curr_dict[name], name, result[name])
    log('got currencies...')
    return res[:-1]


def default_currencies(locale='ru'):
    return get_currencies(default_names, locale=locale)


def currencies_by_query(query, locale='ru'):
    query = query.upper()
    print query
    return get_currencies([query], locale)


def currencies_list(locale='ru'):
    curr_dict = curr_locale_dict[locale]
    res = ''
    for curr in curr_dict.keys():
        res += '{}, '.format(curr)
    return res[:-2]


