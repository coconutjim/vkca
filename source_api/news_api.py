# coding: utf8
__author__ = 'Lev'

from bs4 import BeautifulSoup as Soup
import requests

categories = dict(main='https://news.yandex.ru/index.rss',
                  politics='https://news.yandex.ru/politics.rss',
                  economics='https://news.yandex.ru/business.rss',
                  incidents='https://news.yandex.ru/incident.rss',
                  sport='https://news.yandex.ru/sport.rss',
                  science='https://news.yandex.ru/science.rss',
                  culture='https://news.yandex.ru/culture.rss',
                  religion='https://news.yandex.ru/religion.rss')


def news_by_category(category):
    response = requests.get(categories[category])
    soup = Soup(response.text, features='lxml')
    res = ''
    for item in soup.find_all('item'):
        res += item.find('title').text + '\n'
    return res[:-1]


def default_news():
    return news_by_category('main')


def news_by_query(query):
    response = requests.get(categories['main'])
    soup = Soup(response.text, features='lxml')
    res = ''
    for item in soup.find_all('item'):
        title = item.find('title').text
        description = item.find('description').text
        if query in title or query in description:
            res += title + '\n'
    return res[:-1]


print default_news()





