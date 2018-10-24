import os

from .base import BaseConfig


class Config(BaseConfig):
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS') or '*'
