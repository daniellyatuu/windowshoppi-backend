# Generated by Django 3.1.2 on 2020-10-30 09:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness_post', '0002_auto_20201030_1243'),
        ('master_data', '0003_auto_20201030_1016'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bussiness', '0008_auto_20201030_1243'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Business',
            new_name='Bussiness',
        ),
    ]
