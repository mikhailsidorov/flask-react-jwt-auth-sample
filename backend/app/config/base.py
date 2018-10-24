import os
from datetime import timedelta


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ['REDIS_URL']

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_SESSION_EXPIRES = timedelta(days=30)
