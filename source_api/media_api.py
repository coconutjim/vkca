__author__ = 'Lev'

import requests
import json
import random

from settings import VK_SEARCHING_TOKEN, GCS_KEY, GCS_ID,GIPHY_KEY
from util import log


def image_by_query(query):
    log('getting img url...')
    url = 'https://www.googleapis.com/customsearch/v1?key=' + GCS_KEY + '&cx=' + GCS_ID + '&q=' + query + \
          '&searchType=image&num=10'
    response = requests.get(url)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception('error in api...')
    items = result['items']
    if not items or len(items) == 0:
        log('no image "' + query + '" found')
        return None
    res = list()
    for item in items:
        res.append(item['link'])
    log('got img url...')
    return res[random.randint(0, len(res) - 1)]


def gif_by_query(query):
    log('getting gif utl...')
    url = 'http://api.giphy.com/v1/gifs/search?api_key=' + GIPHY_KEY + '&q=' + query
    response = requests.get(url)
    result = json.loads(response.text)
    if 'error' in result:
        raise Exception('error in api...')
    data = result['data']
    if not data:
        log('no gif "' + query + '" found')
        return None
    res = list()
    for item in data:
        res.append(item['images']['fixed_height_small']['url'])
    log('got gif url...')
    return res[random.randint(0, len(res) - 1)]


def music_by_query(query):
    log('getting audio name...')
    method_url = 'https://api.vk.com/method/audio.search'
    data = dict(access_token=VK_SEARCHING_TOKEN, q=query)
    response = requests.post(method_url, data)
    result = json.loads(response.text)['response']
    if result[0] == 0:
        log('no audio "' + query + '" found')
        return None
    audio = result[random.randint(1, len(result) - 1)]
    log('got audio name...')
    return 'audio' + str(audio['owner_id']) + '_' + str(audio['aid'])


def video_by_query(query):
    log('getting video name...')
    method_url = 'https://api.vk.com/method/video.search'
    data = dict(access_token=VK_SEARCHING_TOKEN, q=query, adult='1')
    response = requests.post(method_url, data)
    result = json.loads(response.text)['response']
    if len(result) == 0:
        log('no video "' + query + '" found')
        return None
    video = result[random.randint(0, len(result) - 1)]
    log('got video name...')
    return 'video' + str(video['owner_id']) + '_' + str(video['id'])
