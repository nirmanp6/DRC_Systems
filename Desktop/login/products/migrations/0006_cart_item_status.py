# Generated by Django 3.1.2 on 2020-10-19 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20201019_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='status',
            field=models.CharField(choices=[('1', 'active'), ('2', 'placed')], default='1', max_length=10),
        ),
    ]
