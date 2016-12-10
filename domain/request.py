__author__ = 'Lev'


class Request:

    def __init__(self, message_id, user_id, date, text):
        self.message_id = message_id
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
