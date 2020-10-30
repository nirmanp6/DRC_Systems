# Generated by Django 3.1.2 on 2020-10-29 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('image', models.ImageField(null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='cart_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('productname', models.CharField(default='', max_length=50)),
                ('productprice', models.FloatField(default=0)),
                ('totalprice', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'placed')], default='1', max_length=10)),
                ('products', models.ManyToManyField(to='products.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'placed')], default='1', max_length=10)),
                ('total', models.FloatField(default=0)),
                ('ordered_date', models.DateTimeField(null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(to='products.cart_item')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
