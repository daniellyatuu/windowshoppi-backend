from .crecidential import *
from .base import *

# print('development server')

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['3.17.145.13', '127.0.0.1', '192.168.1.225']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.'+db_type,
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
        'OPTIONS': {
            'init_command': 'SET sql_mode = "STRICT_TRANS_TABLES"',
        }
    }
}
