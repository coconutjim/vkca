__author__ = 'Lev'

import datetime

from resources import MIN_REQUEST_LENGTH, MAX_REQUEST_LENGTH


class Request:

    def __init__(self, user_id, dt, text):
        if not isinstance(user_id, int):
            raise ValueError('request constructor error: bad user id')
        if isinstance(dt, int):
            dt = datetime.datetime.fromtimestamp(dt).date()
        if not isinstance(dt, datetime.datetime):
            raise ValueError('request constructor error: bad datetime')
        text = str(text)
        if len(text) > MAX_REQUEST_LENGTH:
            raise ValueError('request constructor error: bad text')

        self.user_id = user_id
        self.dt = dt
        self.text = text

        self.type = ''
        self.response_text = ''
        self.attachment = ''
        self.success = False
        self.error_message = ''

    def complete(self):
        pass

    def __repr__(self):
        return '<Request uid:{} date:{} text:{}>'.format(self.user_id, self.dt, self.text)
