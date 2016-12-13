# coding: utf8
__author__ = 'Lev'
import requests
import json
import re
from datetime import datetime

from domain.user import User
from settings import VK_SEARCHING_TOKEN
from util import log
from resources import GENDERS


gender_dict_vk = {0: GENDERS['undef'], 1: GENDERS['F'], 2: GENDERS['M']}
date_pattern = '\d+\.\d+\.\d+'


def get_user_info(user_id, r_date):
    log('getting info for {}'.format(user_id))
    method_url = 'https://api.vk.com/method/users.get?'
    params = dict(access_token=VK_SEARCHING_TOKEN, user_ids=user_id, fields='bdate,sex')
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'searching error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    result = result['response'][0]
    name = result['first_name'] + ' ' + result['last_name']
    b_date = None
    if 'bdate' in result and re.match(date_pattern, result['bdate']) is not None:
        b_date = datetime.strptime(result['bdate'], '%d.%m.%Y').date()
    gender = gender_dict_vk[result['sex']] if 'gender' in result else GENDERS['undef']
    return User(user_id, name, b_date, gender, r_date)
