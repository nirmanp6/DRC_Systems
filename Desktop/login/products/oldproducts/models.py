# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import User

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=10, null=False, unique=True)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/', null=True)
    
    def __str__(self):
        return self.name


class cart_item(models.Model):
    products = models.ManyToManyField(product)
    quantity = models.IntegerField(null=False, default=1)
    user = models.ManyToManyField(User)
    productname = models.CharField(max_length=50, default='')
    productprice = models.FloatField(default=0)
    totalprice = models.FloatField(default=0)


STATUS_CHOICES = (
    ("1", "active"),
    ("2", "placed"),
)

    
class cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    cart_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(cart_item)
    started_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='1')
    total = models.FloatField(default=0)

class order(models.Model):
    cartorder = models.OneToOneField(cart, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)