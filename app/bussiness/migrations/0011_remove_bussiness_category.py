# Generated by Django 3.1.2 on 2020-10-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness', '0010_bussiness_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bussiness',
            name='category',
        ),
    ]
