__author__ = 'Lev'

from Queue import Queue
from time import sleep
from threading import Thread

from vk_api.listening import get_last_message_id, listen_new_requests
from vk_api.sending import send_plain_message
from processing.parser import mock_processor
from util import log
import config

answers_q = Queue()


def q_worker():
    i = 0
    while True:
        # log('checking queue...')
        if answers_q.empty():
            continue
        if i == 1000:
            i = 0
        if i % 4 == 0:
            sleep(1)
        req = answers_q._get()
        try:
            req.complete()
            # write to db
            log('request fully processed...')
        except Exception as e:
            send_plain_message(req.user_id, 'fatal error')  # label
            log('request sending failed with: ' + str(e))
            # write to db
        answers_q.task_done()
        i += 1


def init():
    config.last_message_id = get_last_message_id()
    q_thread = Thread(target=q_worker)
    q_thread.start()


def main():
    try:
        init()
    except Exception as e:
        log(str(e))
        return
    i = 0
    while True:
        if i == 1000:
            i = 0
        if i % 4 == 0:
            sleep(1)
        try:
            reqs = listen_new_requests(config.last_message_id)
        except Exception as e:
            log('fatal: ' + str(e))
            # return
        if len(reqs) != 0:
            config.last_message_id = reqs[0].message_id
            for req in reqs:
                p_thread = Thread(target=mock_processor, kwargs={'req': req})
                p_thread.start()
        i += 1


if __name__ == '__main__':
    main()