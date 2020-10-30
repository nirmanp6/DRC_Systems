from django.contrib import admin
from .models import ProductSignal, UserSignal
# Register your models here.
admin.site.register(ProductSignal)
admin.site.register(UserSignal)