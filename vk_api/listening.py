__author__ = 'Lev'

import requests
import json

from domain.request import Request
from domain.request_factory import build_error_frequency_request
from settings import VK_LISTENING_TOKEN
from util import log
from config import user_attempts, user_spam_warnings, answers_queue


def get_long_poll_server():
    log('getting long poll server...')
    method_url = 'https://api.vk.com/method/messages.getLongPollServer?'
    params = dict(access_token=VK_LISTENING_TOKEN, use_ssl=1)
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception('error in getting long poll server...')
    result = result['response']
    log('got long poll server...')
    return result['server'], result['key'], result['ts']


def long_polling(server, key, ts):
    log('starting long polling...')
    method_url = 'https://' + server
    params = dict(act='a_check', key=key, ts=ts, wait=25, mode=0, version=1)
    response = requests.get(method_url, params=params)
    return json.loads(response.text)


def process_long_polling_results(updates):
    log('found {} update(s)...'.format(len(updates)))
    messages = []
    for update in updates:
        # fuck magic numbers
        if update[0] == 4 and not (update[2] & 2) and update[3] < 2000000000:
            user_id = update[3]
            messages.append(update)
            if user_id not in user_attempts:
                user_attempts[user_id] = 1
            else:
                user_attempts[user_id] += 1

    if len(messages) == 0:
        return messages

    log('found {} message(s)...'.format(len(messages)))
    reqs = []
    for message in messages:
        # fuck magic numbers
        user_id = message[3]
        date = message[4]
        text = message[6]
        if user_attempts[user_id] > 3:
            if user_id not in user_spam_warnings:
                log('detected spam from user {}, adding spam warning...'.format(user_id))
                user_spam_warnings[user_id] = True
                answers_queue.put(build_error_frequency_request(user_id, date))
        else:
            reqs.append(Request(user_id, date, text))
    return reqs


