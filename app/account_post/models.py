from app.master_data.models import HashTag
from app.account.models import Account
from resizeimage import resizeimage
from django.core.files import File
from datetime import datetime
from django.db import models
from io import BytesIO
from PIL import Image
import sys
import os


class AccountPost(models.Model):
    account = models.ForeignKey(
        Account, related_name='account_posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(HashTag)
    caption = models.TextField()
    location_name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=True)
    error_happened_on_uploading_image = models.BooleanField(default=False)
    url = models.URLField(max_length=800, blank=True, null=True)
    url_action_text = models.CharField(max_length=10, blank=True, null=True)
    is_url_valid = models.BooleanField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - :POST FROM: - {}".format(self.id, self.account.name)

    class Meta:
        db_table = 'account_post'
        ordering = ['-id']


class PostImage(models.Model):
    post = models.ForeignKey(
        AccountPost, related_name='post_photos', on_delete=models.CASCADE)
    filename = models.ImageField(upload_to='post_pics')

    # calling image compression function before saving the data
    def save(self, *args, **kwargs):
        new_image = self.compress(self.filename)
        self.filename = new_image
        super().save(*args, **kwargs)

    # image compression method
    def compress(self, filename):
        im = Image.open(filename)

        im = im.convert('RGB')

        # get filename extension
        name, ext = os.path.splitext(filename.name)

        ''' new filename '''
        # current date and time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        new_name = name + str(timestamp)
        new_name = new_name.replace('.', '')

        new_filename = new_name+ext

        max_width = 720
        if im.size[0] > max_width:
            im = resizeimage.resize_width(im, max_width)
        im_io = BytesIO()

        im.save(im_io, 'JPEG', quality=60)
        new_image = File(im_io, name=new_filename)
        return new_image

    def __str__(self):
        return "{}".format(self.filename)

    class Meta:
        db_table = 'post_image'
