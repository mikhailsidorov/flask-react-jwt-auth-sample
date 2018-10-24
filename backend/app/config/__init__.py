import os

ENV_TYPE = os.environ.get('ENV_TYPE')

if ENV_TYPE == 'PROD':
    from .prod import Config
elif ENV_TYPE == 'TESTING':
    from .test import Config
elif ENV_TYPE == 'DEV':
    from .dev import Config
