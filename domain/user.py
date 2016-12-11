__author__ = 'Lev'


class User:

    def __init__(self, user_id, full_name, birth_date, gender, city, country, reg_date):
        self.user_id = user_id
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender
        self.city = city
        self.country = country
        self.reg_date = reg_date

    def __repr__(self):
        return '<User uid:{} name:{} bdate:{} gender:{} city:{} country:{} rdate:{}>'.\
            format(self.user_id, self.full_name, self.birth_date, self.gender,
                   self.city, self.country, self.reg_date)
