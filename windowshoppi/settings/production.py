from .base import *

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['3.16.156.245']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'w_shoppi_db',
        'USER': 'admin',
        'PASSWORD': 'AdminOnly2020',
        'HOST': 'windowshoppi-db.cwn5ckinogze.us-east-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}
