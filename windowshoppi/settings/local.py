from .base import *

DEBUG = True

ALLOWED_HOSTS = []

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