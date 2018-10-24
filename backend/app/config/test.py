import os

from .base import BaseConfig


class Config(BaseConfig):
    TESTING = True
    DEBUG = True
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS') or '*'
