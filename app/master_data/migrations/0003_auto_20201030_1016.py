# Generated by Django 3.1.2 on 2020-10-30 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness_post', '0001_initial'),
        ('bussiness', '0005_auto_20201030_1016'),
        ('master_data', '0002_auto_20200717_2108'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='HashTag',
        ),
        migrations.AlterModelOptions(
            name='hashtag',
            options={},
        ),
    ]