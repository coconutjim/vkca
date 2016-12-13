# coding: utf8

from request import Request
from vk_api.sending import send_plain_message
from resources import RESPONSE_FREQUENT_REQUEST, RESPONSE_DUPLICATE_REQUEST, RESPONSE_REQUEST_LENGTH


def build_error_frequency_request(user_id, dt):
    r = Request(user_id, dt, '')
    r.response_text = RESPONSE_FREQUENT_REQUEST
    r.complete = send_plain_message(user_id, r.response_text)


def build_error_duplicate_request(user_id, dt):
    r = Request(user_id, dt, '')
    r.response_text = RESPONSE_DUPLICATE_REQUEST
    r.complete = send_plain_message(user_id, r.response_text)


def build_error_request_length(user_id, dt):
    r = Request(user_id, dt, '')
    r.response_text = RESPONSE_REQUEST_LENGTH
    r.complete = send_plain_message(user_id, r.response_text)
