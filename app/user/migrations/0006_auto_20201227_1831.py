# Generated by Django 3.1.2 on 2020-12-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20201119_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='call_iso_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='whatsapp_iso_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
