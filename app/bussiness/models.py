from django.db import models
from app.user.models import User
from app.master_data.models import Country, Category


class Bussiness(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='user_bussiness', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='bussiness_category', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    location_name = models.CharField(max_length=255)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    date_registered = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
