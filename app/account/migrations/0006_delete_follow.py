# Generated by Django 3.1.2 on 2021-03-22 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
