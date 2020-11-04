from django.db import models
from app.bussiness.models import Bussiness
from app.master_data.models import HashTag
import sys
from PIL import Image
from io import BytesIO
from django.core.files import File
from resizeimage import resizeimage


class BussinessPost(models.Model):
    bussiness = models.ForeignKey(
        Bussiness, related_name='bussiness_posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(HashTag)
    caption = models.TextField()
    active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{} - Post from {}".format(self.id, self.bussiness.name)


class PostImage(models.Model):
    post = models.ForeignKey(
        BussinessPost, related_name='post_photos', on_delete=models.CASCADE)
    filename = models.ImageField(upload_to='post_pics')

    # # calling image compression function before saving the data
    def save(self, *args, **kwargs):
        new_image = self.compress(self.filename)
        self.filename = new_image
        super().save(*args, **kwargs)

    # image compression method
    def compress(self, filename):
        im = Image.open(filename)

        max_width = 720
        if im.size[0] > max_width:
            im = resizeimage.resize_width(im, max_width)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=60)
        new_image = File(im_io, name=filename.name)
        return new_image

    def __str__(self):
        return "{}".format(self.filename)
