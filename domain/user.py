# coding: utf8

__author__ = 'Lev'

import datetime
from resources import GENDERS


class User:

    def __init__(self, user_id, full_name, birth_date, gender, reg_date):
        if not isinstance(user_id, int):
            raise ValueError('user constructor error: bad user id')
        if not full_name:
            raise ValueError('user constructor error: bad name')
        if isinstance(birth_date, int):
            birth_date = datetime.datetime.fromtimestamp(birth_date).date()
        if birth_date is not None and not isinstance(birth_date, datetime.date):
            raise ValueError('user constructor error: bad bdate')
        if gender not in GENDERS.values():
            raise ValueError('user constructor error: bad gender')
        if isinstance(reg_date, int):
            reg_date = datetime.datetime.fromtimestamp(reg_date).date()
        if not isinstance(reg_date, datetime.date):
            raise ValueError('user constructor error: bad rdate')

        self.user_id = user_id
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender
        self.city = 0
        self.country = 0
        self.reg_date = reg_date

    def __repr__(self):
        return '<User uid:{} name:{} bdate:{} gender:{} city:{} country:{} rdate:{}>'.\
            format(self.user_id, self.full_name, self.birth_date, self.gender,
                   self.city, self.country, self.reg_date)
