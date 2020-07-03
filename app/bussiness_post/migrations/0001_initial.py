# Generated by Django 3.0.7 on 2020-07-02 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bussiness', '0003_bussiness'),
        ('master_data', '0003_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='BussinessPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('bussiness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bussiness_posts', to='bussiness.Bussiness')),
                ('categories', models.ManyToManyField(to='master_data.Category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.ImageField(upload_to='post_pics')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_photos', to='bussiness_post.BussinessPost')),
            ],
        ),
    ]
