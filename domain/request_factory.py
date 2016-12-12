from request import Request
from vk_api.sending import send_plain_message


def build_error_frequency_request(user_id, dt):
    r = Request(user_id, dt, '')
    r.success = False
    r.type = 'undefined'
    r.error_message = 'frequency error'
    r.response_text = 'Too much requests in a short period of time. Please try again later'
    r.complete = send_plain_message(user_id, r.response_text)


def build_error_duplicate_request(user_id, dt):
    r = Request(user_id, dt, '')
    r.success = False
    r.type = 'undefined'
    r.error_message = 'duplicate error'
    r.response_text = 'Duplicate requests in a short period of time. Please try again later'
    r.complete = send_plain_message(user_id, r.response_text)
