# coding: utf8
__author__ = 'Lev'

import re

from vk_api.sending import send_plain_message, send_message_music, send_message_video
from source_api.news_api import default_news, news_by_category, news_by_query
from source_api.weather_api import default_weather, hourly_weather
from source_api.media_api import music_by_query, video_by_query


from resources import MAX_REQUEST_LENGTH
from domain.request_factory import build_error_request_length
from config import answers_queue
from util import log
from db.db_methods import check_user_existence, save_user, get_user_locale, update_user_locale
from vk_api.searching import get_user_info
import config

help_text_ru = u'Вы работаете с Content Aggregator. Список доступных команд:\n' \
               u'Новости\n' \
               u'Новости "запрос"\n' \
               u'Новости "категория" (политика, экономика, происшествия, спорт, наука, культура, религия)\n' \
               u'Погода\n' \
               u'Погода почасовая\n' \
               u'Погода "город"\n' \
               u'Финансы\n' \
               u'Финансы "валюта"\n' \
               u'Финансы "котировка"\n' \
               u'Картинка "запрос"\n' \
               u'Гиф "запрос"\n' \
               u'Музыка "запрос"\n' \
               u'Видео "запрос"\n' \
               u'Смена языка\n' \
               u'Помощь\n' \
               u'Длина запроса должна быть от 1 до 255 символов'

help_text_eng = 'You are dealing with Content Aggregator. List of available commands:\n' \
               'News\n' \
               'News "query"\n' \
               'News "category" (politics, economics, incidents, sport, science, culture, religion)\n' \
               'Weather\n' \
               'Weather hourly\n' \
               'Weather "city"\n' \
               'Finance\n' \
               'Finance "currency"\n' \
               'Finance "stock"\n' \
               'Image "query"\n' \
               'Gif "query"\n' \
               'Music "query"\n' \
               'Video "query"\n' \
               'Change language\n' \
               'Help\n' \
               'Mind that request length should be from 1 up to 255 symbols'


news_cats_dict_eng = dict(politics='Politics', economics='Economics', incidents='Incidents', sport='Sport',
                      science='Science', culture='Culture', religion='Religion')
news_cats_dict_ru = {u'политика':'Politics', u'экономика': 'Economics', u'происшествия':'Incidents',
                     u'спорт':'Sport', u'наука':'Science', u'культура': 'Culture', u'религия':'Religion'}


def parse_eng_request(req, text):
    try:
        if 'help' in text:
            req.category = 'Help'
            req.type = 'Help'
            req.response_text = help_text_eng
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        if 'weather' in text:
            req.category = 'Weather'
            if 'hourly' in text:
                req.type = 'Hourly'
                req.response_text = hourly_weather(locale='eng')
            else:
                req.type = 'Next'
                req.response_text = default_weather(locale='eng')
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        if 'news' in text:
            req.category = 'News'
            req.save = True

            if text.count('&quot;') == 2:
                found = re.findall('&quot;([^"]*)&quot;', text)
                if found is None or len(found) == 0 or found[0] == '':
                    req.type = 'Query'
                    req.success = 0
                    req.response_text = 'Please check request correctness. Query must be in quotes'
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                query = found[0]
                if query in news_cats_dict_eng:
                    req.type = news_cats_dict_eng[query]
                    req.success = 1
                    req.response_text = news_by_category(req.type, locale='eng')
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                req.type = 'Query'
                req.success = 1
                res = news_by_query(query, locale='eng')
                if res == '':
                    res = 'Nothing found by "{}"'.format(query)
                req.response_text = res
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return

            req.type = 'All'
            req.response_text = default_news(locale='eng')

            req.complete = send_plain_message(req.user_id, req.response_text)
            answers_queue.put(req)
            return
        if 'music' in text:
            req.category = 'Music'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = 'Please check request correctness. Query must be in quotes'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = 'Please check request correctness. Query must be in quotes'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            music = music_by_query(query)
            if music is None:
                req.response_text = 'Nothing found by "{}"'.format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = music
                req.complete = send_message_music(req.user_id, '', music)
            answers_queue.put(req)
            return
        if 'video' in text:
            req.category = 'Video'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = 'Please check request correctness. Query must be in quotes'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = 'Please check request correctness. Query must be in quotes'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            video = video_by_query(query)
            if video is None:
                req.response_text = 'Nothing found by "{}"'.format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = video
                req.complete = send_message_video(req.user_id, '', video)
            answers_queue.put(req)
            return
        if 'change language' in text:
            conn = None
            try:
                conn = config.MYSQL_POOL.get_connection()
                update_user_locale(conn, req.user_id, 'ru')
            except Exception as e:
                log(str(e))
                return
            finally:
                if conn is not None:
                    conn.close()
            req.category = 'Locale'
            req.type = 'Change'
            req.response_text = u'Выполнено. Язык сменен на русский'
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        req.category = 'Undefined'
        req.type = 'Undefined'
        req.response_text = 'Unknown request. Try typing "help" command'
        req.success = 0
        req.complete = send_plain_message(req.user_id, req.response_text)
        req.error_message = 'undefined request'
        req.save = True
        answers_queue.put(req)
    except Exception as e:
        log(str(e))
        req.success = 0
        req.error_message = 'error in processing request'
        req.response_text = 'Error in processing request'
        req.complete = send_plain_message(req.user_id, req.answer_text)
        req.save = True
        answers_queue.put(req)


def parse_ru_request(req, text):
    try:
        if u'помощь' in text:
            req.category = 'Help'
            req.type = 'Help'
            req.response_text = help_text_ru
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        if u'погода' in text:
            req.category = 'Weather'
            if u'почасовая' in text:
                req.type = 'Hourly'
                req.response_text = hourly_weather()
            else:
                req.type = 'Next'
                req.response_text = default_weather()
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        if u'новости' in text:
            req.category = 'News'
            req.save = True

            if text.count('&quot;') == 2:
                found = re.findall('&quot;([^"]*)&quot;', text)
                if found is None or len(found) == 0 or found[0] == '':
                    req.type = 'Query'
                    req.success = 0
                    req.response_text = u'Пожалуйста, проверьте правильность написания команды. ' \
                                        u'Запрос должен быть в кавычках'
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                query = found[0]
                if query in news_cats_dict_ru:
                    req.type = news_cats_dict_ru[query]
                    req.success = 1
                    req.response_text = news_by_category(req.type)
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                req.type = 'Query'
                req.success = 1
                res = news_by_query(query)
                if res == '':
                    res = u'К сожалению, по запросу "{}" ничего не найдено'.format(query)
                req.response_text = res
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return

            req.type = 'All'
            req.response_text = default_news()

            req.complete = send_plain_message(req.user_id, req.response_text)
            answers_queue.put(req)
            return
        if u'музыка' in text:
            req.category = 'Music'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = u'Пожалуйста, проверьте правильность написания команды. ' \
                                    u'Запрос должен быть в кавычках'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = u'Пожалуйста, проверьте правильность написания команды. ' \
                                    u'Запрос должен быть в кавычках'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            music = music_by_query(query)
            if music is None:
                req.response_text = u'К сожалению, по запросу "{}" ничего не найдено'.format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = music
                req.complete = send_message_music(req.user_id, '', music)
            answers_queue.put(req)
            return
        if u'видео' in text:
            req.category = 'Video'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = u'Пожалуйста, проверьте правильность написания команды. ' \
                                    u'Запрос должен быть в кавычках'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = u'Пожалуйста, проверьте правильность написания команды. ' \
                                    u'Запрос должен быть в кавычках'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            video = video_by_query(query)
            if video is None:
                req.response_text = u'К сожалению, по запросу "{}" ничего не найдено'.format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = video
                req.complete = send_message_video(req.user_id, '', video)
            answers_queue.put(req)
            return
        if u'смена языка' in text:
            conn = None
            try:
                conn = config.MYSQL_POOL.get_connection()
                update_user_locale(conn, req.user_id, 'eng')
            except Exception as e:
                log(str(e))
                return
            finally:
                if conn is not None:
                    conn.close()
            req.category = 'Locale'
            req.type = 'Change'
            req.response_text = u'Done. Your language is now English'
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        req.category = 'Undefined'
        req.type = 'Undefined'
        req.response_text = u'Неизвестный тип запроса. Попробуйте вызвать команду "помощь"'
        req.success = 0
        req.complete = send_plain_message(req.user_id, req.response_text)
        req.error_message = 'undefined request'
        req.save = True
        answers_queue.put(req)
    except Exception as e:
        log(str(e))
        req.success = 0
        req.error_message = 'error in processing request'
        req.response_text = u'Ошибка в выполнении запроса'
        req.complete = send_plain_message(req.user_id, req.answer_text)
        req.save = True
        answers_queue.put(req)


def process(req):
    text = req.text
    if text is None or text == '' or len(str(text)) > MAX_REQUEST_LENGTH:
        answers_queue.put(build_error_request_length(req.user_id, req.dt))
        return
    conn = None
    locale = 'ru'
    try:
        conn = config.MYSQL_POOL.get_connection()
        user_exists = check_user_existence(conn, req.user_id)
        if not user_exists:
            save_user(conn, get_user_info(req.user_id, req.dt))
            # pass
        else:
            locale = get_user_locale(conn, req.user_id)
    except Exception as e:
        log(str(e))
        return
    finally:
        if conn is not None:
            conn.close()

    text = str(text).decode('utf-8').lower()
    if locale == 'eng':
        parse_eng_request(req, text)
    else:
        parse_ru_request(req, text)




