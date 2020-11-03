# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from slugify import slugify

from django.db import models
from django.contrib.auth.models import User

from signals.models import Signals

# Create your models here.


class product(models.Model):
    '''product model add from admin page
    only, images are uploaded to media
    slug is generated automatically'''
    name = models.CharField(max_length=50, default='', unique=True)
    slug = models.SlugField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='media', null=True)

    def save(self):
        '''had to define custome save method 
        to generate slug so instead of sending 
        post_save signal, sending custom signal'''
        self.slug = slugify(self.name)
        super(product, self).save()
        signal = Signals()
        slug = self.slug
        action = "created"
        signal.product_send(slug=slug, action=action)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ("1", "active"),
    ("2", "placed"),
)


class cart_item(models.Model):
    '''cartitem is unique for
    product+user, quantity and
    price data is stored here'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(product)

    quantity = models.IntegerField(null=False, default=1)
    productname = models.CharField(max_length=50, default='')
    productprice = models.FloatField(default=0)
    totalprice = models.FloatField(default=0)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return self.productname


class cart(models.Model):
    '''carts also handle order 
    details any cart with status=2
    is an order, cart with status=1
    is active right now, quantity 
    field is for dynamic cart'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    cart_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(cart_item)
    started_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='1')
    total = models.FloatField(default=0)
    ordered_date = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=0)
