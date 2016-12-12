__author__ = 'Lev'

from mysql.connector.pooling import MySQLConnectionPool

from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from domain.request import Request
from domain.user import User


dbconfig = {
    'host': DB_HOST,
    'user': DB_USER,
    'database': DB_NAME,
    'password': DB_PASSWORD
}

MYSQL_POOL = None


def init():
    global MYSQL_POOL
    MYSQL_POOL = MySQLConnectionPool(pool_name='my_pool', pool_size=30, **dbconfig)


def check_user_existence(conn, user_id):
    cursor = conn.cursor()
    query = "select UserID from User where UserID = '{}' limit 1".format(user_id)
    cursor.execute(query)
    return cursor.fetchone() is not None


def get_user_locale(conn, user_id):
    cursor = conn.cursor()
    query = "select LocaleID from UserSettings where UserID = '{}' limit 1".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return None
    query = "select Name from Locale where id = '{}'".format(result[0])
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result is not None else None


def update_user_locale(conn, user_id, locale):
    cursor = conn.cursor()
    query = "select id from Locale where Name = '{}'".format(locale)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        loc_id = result[0]
        query = "select UserID from UserSettings where UserID = '{}' limit 1".format(user_id)
        cursor.execute(query)
        r = cursor.fetchone()
        if r is None:
            query = "insert into UserSettings (UserID, LocaleID) values ('{}', '{}')".format(user_id, loc_id)
        else:
            query = "update UserSettings set LocaleId = '{}' where UserID = '{}'".format(loc_id, user_id)
        cursor.execute(query)
        conn.commit()


def get_last_user_request_time(conn, user_id):
    cursor = conn.cursor()
    query = "select ReqTime from Request where UserID = '{}' order by Reqtime desc limit 1".format(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return None if result is None else result[0]


def save_user(conn, user):
    cursor = conn.cursor()
    # consider that it can be datetime, not date here, but db processes it
    query = "insert into User (UserID, FullName, BirthDate, Gender, RegDate) values \
        ({}, '{}', '{}', '{}', '{}')".format(user.user_id, user.full_name, user.birth_date,
                                     user.gender, user.reg_date)
    cursor.execute(query)
    conn.commit()


def save_request(conn, request):
    cursor = conn.cursor()
    query = "select id from Type where TypeName = '{}' limit 1".format(request.type)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        raise Exception('db error: type {} was not found!'.format(request.type))
    type_id = result[0]
    query = "insert into Log (ErrorMessage, Text, ResponseText) values ('{}', '{}', '{}')"\
        .format(request.error_message, request.text, request.response_text)
    cursor.execute(query)
    log_id = cursor.lastrowid
    query = "insert into Request (ReqTime, TypeID, UserID, IsSuccess, LogId, SessionID)"\
        .format(request.dt, type_id, request.user_id, request.success, log_id, request.session_id)
    cursor.execute(query)
    conn.commit()


def create_session(conn, dt):
    cursor = conn.cursor()
    query = "insert into Session (StartTime) values ('{}')".format(dt)
    cursor.execute(query)
    ses_id = cursor.lastrowid
    conn.commit()
    return ses_id



def get_all_users(conn):
    cursor = conn.cursor()
    query = 'select * from User'
    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        print user


def get_all_requests(conn):
    cursor = conn.cursor()
    query = 'select * from Request'
    cursor.execute(query)
    reqs = cursor.fetchall()
    for req in reqs:
        print req

'''
print 1
init()
print 2
conn = MYSQL_POOL.get_connection()
get_all_users(conn)
conn.close()
'''
