# Generated by Django 3.1.2 on 2020-10-30 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness', '0007_auto_20201030_1243'),
        ('bussiness_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bussinesspost',
            name='bussiness',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bussiness_posts', to='bussiness.business'),
        ),
    ]
