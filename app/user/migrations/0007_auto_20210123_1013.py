# Generated by Django 3.1.2 on 2021-01-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20201227_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='call_dial_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='whatsapp_dial_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
