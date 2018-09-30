import os
from datetime import timedelta


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ['REDIS_URL']

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
