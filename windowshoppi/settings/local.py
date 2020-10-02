from .crecidential import *
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.70', '3.17.145.13']

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
