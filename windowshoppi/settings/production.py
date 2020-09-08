from .base import *
from .crecidential import *

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '3.17.145.13']

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
