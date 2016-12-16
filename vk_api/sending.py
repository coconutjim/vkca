# coding: utf8
__author__ = 'Lev'

import requests
import json
from StringIO import StringIO

from settings import VK_ANSWERING_TOKEN, VK_ATTACHMENTS_COMMUNITY_ID
from util import log

POSTING_IMG_TIMEOUT = 20
POSTING_GIF_TIMEOUT = 20


def send_plain_message(user_id, text):
    log('sending text...')
    method_url = 'https://api.vk.com/method/messages.send?'
    data = dict(access_token=VK_ANSWERING_TOKEN, user_id=user_id, message=text)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'sending error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    log('sent text...')


def load_img(img_url):
    response = requests.get(img_url)
    img_data = StringIO(response.content)
    img = {'photo': ('img.jpg', img_data)}

    log('getting upload server for image...')
    method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    params = dict(access_token=VK_ANSWERING_TOKEN, gid=VK_ATTACHMENTS_COMMUNITY_ID)
    response = requests.get(method_url, params=params)
    result = json.loads(response.text)
    upload_url = result['response']['upload_url']

    log('posting image to server...')
    response = requests.post(upload_url, files=img, timeout=POSTING_IMG_TIMEOUT)
    result = json.loads(response.text)
    log('posted image...')

    log('getting image link...')
    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    data = dict(access_token=VK_ANSWERING_TOKEN, gid=VK_ATTACHMENTS_COMMUNITY_ID,
                photo=result['photo'], hash=result['hash'], server=result['server'])
    response = requests.post(method_url, data)
    log('got image link...')
    return json.loads(response.text)['response'][0]['id']


def send_message_image(user_id, text, img_url):
    img_name = load_img(img_url)
    log('sending image...')
    method_url = 'https://api.vk.com/method/messages.send?'
    data = dict(access_token=VK_ANSWERING_TOKEN, user_id=user_id, message=text, attachment=img_name)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'sending error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    log('sent image...')


def load_gif(gif_url):
    response = requests.get(gif_url)
    img_data = StringIO(response.content)
    img = {'file': ('img.gif', img_data)}

    log('getting upload server for gif..')
    method_url = 'https://api.vk.com/method/docs.getUploadServer?'
    data = dict(access_token=VK_ANSWERING_TOKEN, group_id=VK_ATTACHMENTS_COMMUNITY_ID)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    upload_url = result['response']['upload_url']
    log('got upload server..')

    log('posting gif to server')
    response = requests.post(upload_url, files=img, timeout=POSTING_GIF_TIMEOUT)
    result = json.loads(response.text)
    log('posted gif..')

    log('getting gif link..')
    method_url = 'https://api.vk.com/method/docs.save?'
    data = dict(access_token=VK_ANSWERING_TOKEN, file=result['file'], title='gif')
    response = requests.post(method_url, data)
    result = json.loads(response.text)['response'][0]
    log('got gif link..')
    gif_name = 'doc' + str(result['owner_id']) + '_' + str(result['did'])
    return gif_name


def send_message_gif(user_id, text, gif_url):
    gif_name = load_gif(gif_url)
    log('sending gif...')
    method_url = 'https://api.vk.com/method/messages.send?'
    data = dict(access_token=VK_ANSWERING_TOKEN, user_id=user_id, message=text, attachment=gif_name)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'sending error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    log('sent gif...')


def send_message_music(user_id, text, audio_name):
    log('sending audio...')
    method_url = 'https://api.vk.com/method/messages.send?'
    data = dict(access_token=VK_ANSWERING_TOKEN, user_id=user_id, message=text, attachment=audio_name)
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'sending error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    log('sent audio...')


def send_message_video(user_id, text, video_name):
    log('sending video...')
    data = dict(access_token=VK_ANSWERING_TOKEN, user_id=user_id, message=text, attachment=video_name)
    method_url = 'https://api.vk.com/method/messages.send?'
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    if 'error' in result:
        error = 'sending error({}): {}'.format(result['error']['error_code'], result['error']['error_msg'])
        raise Exception(error)
    log('sent video...')

