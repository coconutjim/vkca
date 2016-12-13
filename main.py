# coding: utf8
__author__ = 'Lev'

from time import sleep
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from db.db_methods import init_mysql_pool, save_request
from vk_api.listening import get_long_poll_server, long_polling, process_long_polling_results
from vk_api.sending import send_plain_message
from processing.processor import process
from util import log
import config
from config import answers_queue, user_attempts, user_spam_warnings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def user_attempts_worker():
    while True:
        sleep(5)
        user_attempts.clear()
        user_spam_warnings.clear()


def answers_worker():
    i = 0
    while True:
        # log('checking queue...')
        if answers_queue.empty():
            continue
        if i == 1000:
            i = 0
        if i % 4 == 0:
            sleep(1)
        req = answers_queue._get()
        if req is None:
            continue
        try:
            if req.save:
                conn = None
                try:
                    conn = config.MYSQL_POOL.get_connection()
                    save_request(conn, req)
                except Exception as e:
                    log(str(e))
                finally:
                    if conn is not None:
                        conn.close()
            req.complete()
            log('request fully processed...')
        except Exception as e:
            pass
            #log('request sending failed with: ' + str(e))
            #send_plain_message(req.user_id, '')  # label
            # write to db
        answers_queue.task_done()
        i += 1


def process_requests(pool, data):
    reqs = process_long_polling_results(data)
    for req in reqs:
        pool.submit(process, req)


def main():
    init_mysql_pool()
    answers_thread = Thread(target=answers_worker)
    answers_thread.setDaemon(True)
    answers_thread.start()
    user_attempts_thread = Thread(target=user_attempts_worker)
    user_attempts_thread.setDaemon(True)
    user_attempts_thread.start()

    pool = ThreadPoolExecutor(10)
    server, key, ts = get_long_poll_server()

    while True:
        result = long_polling(server, key, ts)
        if 'failed' in result:
            log('fail in long polling, restarting it...')
            server, key, new_ts_unused = get_long_poll_server()
        else:
            ts = result['ts']
            # pool.submit(process_requests, pool, result['updates'])
            reqs = process_long_polling_results(result['updates'])
            for req in reqs:
                pool.submit(process, req)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(str(e))
