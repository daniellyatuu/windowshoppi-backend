from .base import *
from .crecidential import *

# print('production server')

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

ALLOWED_HOSTS = ['3.17.145.13']

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
