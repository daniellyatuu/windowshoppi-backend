from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    ios2 = models.CharField(max_length=50)
    language = models.CharField(max_length=100)
    country_code = models.IntegerField()
    timezone = models.CharField(max_length=100)
    # flag = models.
    active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    visited = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
