from django.db import models
from app.user.models import User
from app.master_data.models import Country, HashTag


class Bussiness(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='user_business', on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_pics_demo', blank=True, null=True)  # upload_to = 'profile_pics'
    bio = models.TextField(blank=True, null=True)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Business'
