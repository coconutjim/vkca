from request import Request
from vk_api.sending import send_plain_message


def build_error_frequency_request(user_id, date):
    r = Request(user_id, date, '')
    r.type = 0
    r.category = 'undefined'
    r.error_message = 'frequency error'
    r.answer_text = 'Too much requests in a short period of time. Please try again later'
    r.complete = send_plain_message(user_id, r.answer_text)
