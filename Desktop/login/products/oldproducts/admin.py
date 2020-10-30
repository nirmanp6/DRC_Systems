# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . models import product, cart, order, cart_item
from django.contrib import admin

# Register your models here.
admin.site.register(product)
admin.site.register(cart)
admin.site.register(order)
admin.site.register(cart_item)