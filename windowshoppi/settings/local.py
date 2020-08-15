from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.62', '192.168.43.155']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'windowshoppi',
        'USER': 'root',
        'PASSWORD': 'Zomper',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
