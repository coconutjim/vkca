# coding: utf8
__author__ = 'Lev'

from bs4 import BeautifulSoup as Soup
from settings import YANDEX_TRANSLATE_KEY
import requests
from util import log
import json

categories = dict(Main='https://news.yandex.ru/index.rss',
                  Politics='https://news.yandex.ru/politics.rss',
                  Economics='https://news.yandex.ru/business.rss',
                  Incidents='https://news.yandex.ru/incident.rss',
                  Sport='https://news.yandex.ru/sport.rss',
                  Science='https://news.yandex.ru/science.rss',
                  Culture='https://news.yandex.ru/culture.rss',
                  Religion='https://news.yandex.ru/religion.rss')


def news_by_category(category, locale='ru'):
    response = requests.get(categories[category])
    soup = Soup(response.text, features='lxml')
    res = ''
    for item in soup.find_all('item'):
        res += item.find('title').text + '\n'
    res = res[:-1]
    return translate_text(res) if locale == 'eng' else res


def default_news(locale='ru'):
    return news_by_category('Main', locale=locale)


def translate_text(text):
    log('translating text...')
    data = dict(key=YANDEX_TRANSLATE_KEY, lang='en', text=text)
    method_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    response = requests.post(method_url, data)
    translation = json.loads(response.text)['text'][0]
    log('translated text...')
    return translation


def news_by_query(query, locale='ru'):
    res = ''
    for k, v in categories.iteritems():
        response = requests.get(v)
        soup = Soup(response.text, features='lxml')
        for item in soup.find_all('item'):
            title = item.find('title').text
            description = item.find('description').text
            if query in title.lower() or query in description.lower():
                res += title + '\n'
    if res == '':
        return ''
    res = res[:-1]
    return translate_text(res) if locale == 'eng' else res






