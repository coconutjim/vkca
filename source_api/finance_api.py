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
    eng_dict = json.loads(response.text)
    log('got currencies dictionary...')
    to_tr = ''
    for v in eng_dict.values():
        to_tr += v + '\n'
    arr = translate_text(to_tr[:-1], lang='ru').split('\n')
    ru_dict = dict()
    i = 0
    for k in eng_dict.keys():
        ru_dict[k] = arr[i]
        i += 1
    return eng_dict, ru_dict


eng_dict, ru_dict = get_currency_dictionaries()

curr_locale_dict = dict(ru=ru_dict, eng=eng_dict)
label_locale_dict = dict(ru=u'Курсы валют по отношению к американскому доллару (USD):\n',
                         eng='Currencies based on USD:\n')


def default_currencies(locale='ru'):
    log('getting currencies...')
    method_url = API_URL + 'latest.json'
    params = dict(app_id=FINANCE_APP_ID)
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)['rates']
    res = label_locale_dict[locale]
    curr_dict = curr_locale_dict[locale]
    for k, v in result.iteritems():
        res += '{} ({}) - {}\n'.format(curr_dict[k], k, v)
    return res[:-1]

