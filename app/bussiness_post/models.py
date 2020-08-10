from django.db import models
from app.bussiness.models import Bussiness
from app.master_data.models import Category
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


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

    # # calling image compression function before saving the data
    # def save(self, *args, **kwargs):
    #     print('pass in here')
    #     # new_image = compress(self.filename)
    #     # self.filename = new_image
    #     super().save(*args, **kwargs)

    # # image compression method
    # def compress(filename):
    #     im = Image.open(filename)
    #     print(im)
    #     im_io = BytesIO()
    #     im.save(im_io, 'JPEG', quality=60)
    #     new_image = File(im_io, name=filename.name)
    #     return new_image
