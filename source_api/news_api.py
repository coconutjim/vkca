# coding: utf8
__author__ = 'Lev'

from bs4 import BeautifulSoup as Soup
import requests


from api_utils import translate_text
from util import log

categories = dict(Main='https://news.yandex.ru/index.rss',
                  Politics='https://news.yandex.ru/politics.rss',
                  Economics='https://news.yandex.ru/business.rss',
                  Incidents='https://news.yandex.ru/incident.rss',
                  Sport='https://news.yandex.ru/sport.rss',
                  Science='https://news.yandex.ru/science.rss',
                  Culture='https://news.yandex.ru/culture.rss',
                  Religion='https://news.yandex.ru/religion.rss')


def news_by_category(category, locale='ru'):
    log("getting news '{}'...".format(category))
    response = requests.get(categories[category])
    soup = Soup(response.text, features='lxml')
    res = ''
    for item in soup.find_all('item'):
        res += item.find('title').text + '\n'
    res = res[:-1]
    log('got news...')
    return translate_text(res) if locale == 'eng' else res


def default_news(locale='ru'):
    return news_by_category('Main', locale=locale)


def news_by_query(query, locale='ru'):
    log("getting news '{}'...".format(query))
    raw = ''
    for k, v in categories.iteritems():
        response = requests.get(v)
        soup = Soup(response.text, features='lxml')
        for item in soup.find_all('item'):
            raw += item.find('title').text + '\n'
    raw = raw[:-1]
    arr = set(translate_text(raw).split('\n') if locale == 'eng' else raw.split('\n'))
    res = ''
    for item in arr:
        if query in item.lower():
            res += item + '\n'
    if res == '':
        return ''
    res = res[:-1]
    log('got news...')
    return translate_text(res) if locale == 'eng' else res






