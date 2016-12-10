__author__ = 'Lev'

import requests
import json

from domain.request import Request
from settings import VK_LISTENING_TOKEN
from util import log


def get_last_message_id():
    log('getting last message id...')
    data = dict(access_token=VK_LISTENING_TOKEN, out=0, count=1)
    method_url = 'https://api.vk.com/method/messages.get?'
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception('fatal error in listening')
    messages = result['response']
    if len(messages) < 2:
        return 0
    log('got last message id...')
    return messages[1]['mid']


def listen_new_requests(last_message_id):
    # counter user frequency
    # log('listening requests...')
    data = dict(access_token=VK_LISTENING_TOKEN, out=0, count=200, preview_length=0, last_message_id=last_message_id)
    method_url = 'https://api.vk.com/method/messages.get?'
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception('fatal error in listening')
    reqs = []
    messages = result['response']
    if len(messages) < 2:
        return reqs
    for message in messages[1:]:
        if 'chat_id' not in message:
            reqs.append(Request(message['mid'], message['uid'], message['date'], message['body']))
    log('got ' + str(len(reqs)) + ' new request(s)...')
    return reqs


