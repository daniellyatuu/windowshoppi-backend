from windowshoppi.settings.base import MEDIA_URL
from django.contrib.auth.models import Group
from app.master_data.models import HashTag
from app.user.models import User
from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='user_account', on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile_picture', blank=True, null=True)
    account_bio = models.TextField(blank=True, null=True)
    business_bio = models.TextField(max_length=30, blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'account'
        ordering = ['-id']
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return '{}'.format(self.name)

    def profile_photo(self):
        if(self.profile_image):
            return MEDIA_URL + str(self.profile_image)
