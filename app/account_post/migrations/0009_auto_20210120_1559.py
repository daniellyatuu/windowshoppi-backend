# Generated by Django 3.1.2 on 2021-01-20 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_post', '0008_auto_20210120_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountpost',
            name='url',
            field=models.URLField(blank=True, max_length=800, null=True),
        ),
    ]
