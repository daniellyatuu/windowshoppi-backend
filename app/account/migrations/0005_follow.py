# Generated by Django 3.1.2 on 2021-03-22 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_business_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='account.account')),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='account.account')),
            ],
            options={
                'db_table': 'follow',
                'ordering': ['-id'],
            },
        ),
    ]