# Generated by Django 3.0.7 on 2020-07-17 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bussiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('location_name', models.CharField(max_length=255)),
                ('lattitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bussiness_category', to='master_data.Category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_data.Country')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
