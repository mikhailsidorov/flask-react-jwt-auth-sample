import os

from .base import BaseConfig


class Config(BaseConfig):
    SECRET_KEY = os.environ['SECRET_KEY']

    ALLOWED_ORIGINS = os.environ['ALLOWED_ORIGINS']
