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

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.flag = self.compressImage(self.flag)
    #     super(Country, self).save(*args, **kwargs)

    # def compressImage(self, flag):
    #     imageTemproary = Image.open(flag)
    #     outputIoStream = BytesIO()

    #     # get file size
    #     filesize = flag.file.size
    #     filename = str(flag.file)
    #     file_extension = filename.split(".")[-1]
    #     if file_extension == 'jpg':
    #         print('pass in here')
    #         file_extension == 'JPEG'
    #     print(file_extension)

    #     imageTemproary.save(outputIoStream, format=file_extension, quality=60)
    #     outputIoStream.seek(0)

    #     flagImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % flag.name.split('.')[
    #         0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
    #     return flagImage


class Category(models.Model):
    name = models.CharField(max_length=100)
    visited = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
