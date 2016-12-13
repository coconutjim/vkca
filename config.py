# coding: utf8
__author__ = 'Lev'

from Queue import Queue

last_message_id = 0

answers_queue = Queue()

user_attempts = dict()
user_spam_warnings = dict()

MYSQL_POOL = None

