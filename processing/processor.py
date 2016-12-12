# coding: utf8
__author__ = 'Lev'

from vk_api.sending import send_plain_message
from source_api.news_api import default_news
from source_api.weather_api import default_weather



import requests
import json
from settings import WORD_KEY



def mock_processor(req):
    # write user to db if needed
    # process empty body
    text = req.text
    if text is None or text == '':
        return
    text = text.lower()

    req.type = ''
    req.attachment = ''

    try:
        response = requests.get('http://api.wordnik.com/v4/words.json/randomWord?api_key=' + WORD_KEY)
        req.answer_text = json.loads(response.text)['word']
        if u'погода' in text:
            req.answer_text = default_weather()
        if u'новости' in text:
            req.answer_text = default_news()
        req.success = True
        req.error_message = ''
        req.complete = send_plain_message(req.user_id, req.answer_text)
    except Exception as e:
        req.success = False
        req.error_message = str(e)
        req.complete = send_plain_message(req.user_id, req.error.message)
