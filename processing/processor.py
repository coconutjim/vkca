# coding: utf8
__author__ = 'Lev'

import re

from vk_api.sending import send_plain_message, send_message_music, send_message_video
from source_api.news_api import default_news, news_by_category, news_by_query
from source_api.weather_api import default_weather, hourly_weather
from source_api.finance_api import default_currencies, currencies_by_query, currencies_list
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
               u'Валюты\n' \
               u'Валюты "запрос"' \
               u'Валюты список' \
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
                'Currencies\n' \
                'Currencies "query"\n' \
                'Currencies list\n' \
                'Image "query"\n' \
                'Gif "query"\n' \
                'Music "query"\n' \
                'Video "query"\n' \
                'Change language\n' \
                'Help\n' \
                'Mind that request length should be from 1 up to 255 symbols'

help_text_dict = dict(ru=help_text_ru, eng=help_text_eng)

news_cats_dict_eng = dict(politics='Politics', economics='Economics', incidents='Incidents', sport='Sport',
                          science='Science', culture='Culture', religion='Religion')
news_cats_dict_ru = {u'политика': 'Politics', u'экономика': 'Economics', u'происшествия':'Incidents',
                     u'спорт': 'Sport', u'наука': 'Science', u'культура': 'Culture', u'религия': 'Religion'}

news_cats_dict = dict(ru=news_cats_dict_ru, eng=news_cats_dict_eng)


stopwords_dict_eng = dict(help='help', news='news', weather='weather', hourly='hourly', currencies='currencies',
                          list='list', music='music', video='video', locale='change language')

stopwords_dict_ru = dict(help=u'помощь', news=u'новости', weather=u'погода', hourly=u'почасовая', currencies=u'валюты',
                         list=u'список', music=u'музыка', video=u'видео', locale=u'смена языка')

stopwords_dict = dict(ru=stopwords_dict_ru, eng=stopwords_dict_eng)

quotes_message_dict = dict(ru=u'Пожалуйста, проверьте правильность написания команды. Запрос должен быть в кавычках',
                           eng='Please check request correctness. Query must be in quotes')

not_found_message_dict = dict(ru=u'К сожалению, по запросу "{}" ничего не найдено', eng='Nothing found by "{}"')

change_locale_message_dict = dict(ru='Done. Your language is now English', eng=u'Выполнено. Язык сменен на русский')

locale_to_change_dict = dict(ru='eng', eng='ru')

unknown_req_message_dict = dict(ru=u'Неизвестный тип запроса. Попробуйте вызвать команду "помощь"',
                                eng='Unknown request. Try typing "help" command')

processing_err_message_dict = dict(ru=u'Ошибка в выполнении запроса',
                                   eng='Error in processing request')

incorrect_currency_message = dict(ru=u'К сожалению, валюта "{}" не найдена. Попробуйте вызвать "валюты список" '
                                     u'для получения списка доступных валют',
                                  eng='Currency "{}" not found. Try "currencies list" to monitor available currencies')


def parse_request(req, text, locale='ru'):
    sws = stopwords_dict[locale]
    try:
        if sws['help'] in text:
            req.category = 'Help'
            req.type = 'Help'
            req.response_text = help_text_dict[locale]
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        if sws['news'] in text:
            req.category = 'News'
            req.save = True
            if text.count('&quot;') == 2:
                found = re.findall('&quot;([^"]*)&quot;', text)
                if found is None or len(found) == 0 or found[0] == '':
                    req.type = 'Query'
                    req.success = 0
                    req.response_text = quotes_message_dict[locale]
                    req.error_message = 'empty query'
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                query = found[0]
                cats_dict = news_cats_dict[locale]
                if query in cats_dict:
                    req.type = cats_dict[query]
                    req.success = 1
                    req.response_text = news_by_category(req.type, locale=locale)
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                req.type = 'Query'
                req.success = 1
                res = news_by_query(query, locale=locale)
                if res == '':
                    res = not_found_message_dict[locale].format(query)
                req.response_text = res
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return

            req.type = 'All'
            req.response_text = default_news(locale=locale)
            req.complete = send_plain_message(req.user_id, req.response_text)
            answers_queue.put(req)
            return
        if sws['weather'] in text:
            req.category = 'Weather'
            req.save = True
            if sws['hourly'] in text:
                req.type = 'Hourly'
                req.response_text = hourly_weather(locale=locale)
            else:
                req.type = 'Next'
                req.response_text = default_weather(locale=locale)
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            answers_queue.put(req)
            return
        if sws['currencies'] in text:
            req.category = 'Finance'
            req.save = True
            if sws['list'] in text:
                req.type = 'Currencies_list'
                req.success = 1
                req.response_text = currencies_list(locale=locale)
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            if text.count('&quot;') == 2:
                req.type = 'Currencies_query'
                found = re.findall('&quot;([^"]*)&quot;', text)
                if found is None or len(found) == 0 or found[0] == '':
                    req.success = 0
                    req.response_text = quotes_message_dict[locale]
                    req.error_message = 'empty query'
                    req.complete = send_plain_message(req.user_id, req.response_text)
                    answers_queue.put(req)
                    return
                query = found[0]
                req.success = 1
                res = currencies_by_query(query, locale)
                if res == '':
                    res = incorrect_currency_message[locale].format(query)
                req.response_text = res
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            req.type = 'Currencies'
            req.success = 1
            req.response_text = default_currencies(locale=locale)
            req.complete = send_plain_message(req.user_id, req.response_text)
            answers_queue.put(req)
            return
        if sws['music'] in text:
            req.category = 'Music'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = quotes_message_dict[locale]
                req.error_message = 'incorrect query'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = quotes_message_dict[locale]
                req.error_message = 'empty query'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            music = music_by_query(query)
            if music is None:
                req.response_text = not_found_message_dict[locale].format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = music
                req.complete = send_message_music(req.user_id, '', music)
            answers_queue.put(req)
            return
        if sws['video'] in text:
            req.category = 'Video'
            req.type = 'Query'
            req.save = True
            if text.count('&quot;') != 2:
                req.success = 0
                req.response_text = quotes_message_dict[locale]
                req.error_message = 'incorrect query'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            found = re.findall('&quot;([^"]*)&quot;', text)
            if found is None or len(found) == 0 or found[0] == '':
                req.success = 0
                req.response_text = quotes_message_dict[locale]
                req.error_message = 'empty query'
                req.complete = send_plain_message(req.user_id, req.response_text)
                answers_queue.put(req)
                return
            query = found[0]
            req.success = 1
            video = video_by_query(query)
            if video is None:
                req.response_text = not_found_message_dict[locale].format(query)
                req.complete = send_plain_message(req.user_id, req.response_text)
            else:
                req.response_text = video
                req.complete = send_message_video(req.user_id, '', video)
            answers_queue.put(req)
            return
        if sws['locale'] in text:
            conn = None
            try:
                conn = config.MYSQL_POOL.get_connection()
                update_user_locale(conn, req.user_id, locale_to_change_dict[locale])
            except Exception as e:
                log(str(e))
                return
            finally:
                if conn is not None:
                    conn.close()
            req.category = 'Locale'
            req.type = 'Change'
            req.response_text = change_locale_message_dict[locale]
            req.success = 1
            req.complete = send_plain_message(req.user_id, req.response_text)
            req.save = True
            answers_queue.put(req)
            return
        req.category = 'Undefined'
        req.type = 'Undefined'
        req.response_text = unknown_req_message_dict[locale]
        req.success = 0
        req.complete = send_plain_message(req.user_id, req.response_text)
        req.error_message = 'undefined request'
        req.save = True
        answers_queue.put(req)
    except Exception as e:
        log(str(e))
        req.success = 0
        req.error_message = 'error in processing request'
        req.response_text = processing_err_message_dict[locale]
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
    parse_request(req, text, locale)



