# Generated by Django 3.1.2 on 2020-11-19 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20201119_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='business_bio',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
    ]