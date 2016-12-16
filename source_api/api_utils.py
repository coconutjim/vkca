# coding: utf8
__author__ = 'Lev'

import requests
import json

from settings import YANDEX_TRANSLATE_KEY
from util import log


def translate_text(text, lang='en'):
    log('translating text...')
    data = dict(key=YANDEX_TRANSLATE_KEY, lang=lang, text=text)
    method_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    response = requests.post(method_url, data)
    translation = json.loads(response.text)['text'][0]
    log('translated text...')
    return translation
