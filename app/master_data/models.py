import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Country(models.Model):
    name = models.CharField(max_length=100)
    ios2 = models.CharField(max_length=50)
    language = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='flag_pics')
    active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class HashTag(models.Model):
    name = models.CharField(max_length=100)
    visited = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
