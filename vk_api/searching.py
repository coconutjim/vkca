__author__ = 'Lev'
import requests
import json
import re
from datetime import datetime

from domain.user import User
from settings import VK_SEARCHING_TOKEN
from util import log

gender_dict = {0: None, 1: 'F', 2: 'M'}
date_pattern = '\d+\.\d+\.\d+'


def get_user_info(user_id, date):
    log('getting info for {}'.format(user_id))
    method_url = 'https://api.vk.com/method/users.get?'
    params = dict(access_token=VK_SEARCHING_TOKEN, user_ids=user_id, fields='bdate,sex,city,country')
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'searching error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    result = result['response'][0]
    name = result['first_name'] + ' ' + result['last_name']
    bdate = None
    if re.match(date_pattern, result['bdate']) is not None:
        dt = datetime.strptime(result['bdate'], '%d.%m.%Y')
        bdate = int((dt - datetime(1970, 1, 1)).total_seconds())
    gender = gender_dict[result['sex']]
    city = result['city']  # TODO: consider
    country = result['country']  # TODO: consider
    return User(user_id, name, bdate, gender, city, country, date)
