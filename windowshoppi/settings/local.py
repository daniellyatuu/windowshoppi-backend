from .base import *
from .crecidential import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.62', '192.168.43.155']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.'+db_type,
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}
