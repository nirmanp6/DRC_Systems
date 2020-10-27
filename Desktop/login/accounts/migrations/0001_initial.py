# Generated by Django 3.1.2 on 2020-10-15 05:58

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('f_name', models.CharField(default='', max_length=30)),
                ('country', models.CharField(default='', max_length=30)),
                ('mobile', models.IntegerField(default='0')),
                ('address', models.CharField(default='', max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, accounts.models.UserManager),
        ),
    ]
