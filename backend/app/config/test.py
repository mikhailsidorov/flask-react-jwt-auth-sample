import os

from .base import BaseConfig


class Config(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_TESTING']
