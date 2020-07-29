from django.db import models
from app.bussiness.models import Bussiness
from app.master_data.models import Category


class BussinessPost(models.Model):
    bussiness = models.ForeignKey(
        Bussiness, related_name='bussiness_posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    caption = models.TextField()
    active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class PostImage(models.Model):
    post = models.ForeignKey(
        BussinessPost, related_name='post_photos', on_delete=models.CASCADE)
    filename = models.ImageField(upload_to='post_pics')
