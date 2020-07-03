from django.db import models
from app.user.models import User
from app.master_data.models import Category

class Bussiness(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='user_bussiness', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='bussiness_category', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    location_name = models.CharField(max_length=255)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    date_registered = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

