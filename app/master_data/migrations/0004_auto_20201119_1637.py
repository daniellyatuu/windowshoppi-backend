# Generated by Django 3.1.2 on 2020-11-19 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0003_auto_20201030_1016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hashtag',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelTable(
            name='hashtag',
            table='hashtag',
        ),
    ]
