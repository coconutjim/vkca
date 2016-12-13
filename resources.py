# coding: utf8

MIN_REQUEST_LENGTH = 1
MAX_REQUEST_LENGTH = 255

GENDERS = dict(M='M', F='F', undef='')

LOCALES = dict(eng='eng', ru='ru')


RESPONSE_FREQUENT_REQUEST = u'Слишком много запросов в короткий промежуток времени. Попробуйте позже'
RESPONSE_DUPLICATE_REQUEST = u'Повторящиеся запросы в короткий промежуток времени. Попробуйте позже'
RESPONSE_REQUEST_LENGTH = u'Некорректная длина запроса. Длина запроса должна быть от 1 до 255 символов'