# Generated by Django 3.1.2 on 2021-02-14 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_post', '0009_auto_20210120_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountpost',
            name='post_type',
            field=models.IntegerField(choices=[(1, 'normal-post'), (1, 'recommendation')], default=1),
        ),
        migrations.AddField(
            model_name='accountpost',
            name='recommendation_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountpost',
            name='recommendation_phone_dial_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='accountpost',
            name='recommendation_phone_iso_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='accountpost',
            name='recommendation_phone_number',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')]),
        ),
        migrations.AddField(
            model_name='accountpost',
            name='recommendation_type',
            field=models.IntegerField(blank=True, choices=[(1, 'business'), (1, 'product'), (1, 'place')], null=True),
        ),
    ]
