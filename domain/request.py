__author__ = 'Lev'


class Request:

    def __init__(self, user_id, date, text):
        self.user_id = user_id
        self.date = date
        self.text = text

        self.type = 0
        self.category = ''
        self.answer_text = ''
        self.attachment = ''
        self.success = False
        self.error_message = ''

    def complete(self):
        pass

    def __repr__(self):
        return '<Request uid:{} date:{} text:{}>'.format(self.user_id, self.date, self.text)
