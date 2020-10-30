from django.contrib import admin

from .models import Profile, Emails
# Register your models here.
admin.site.register(Profile)
admin.site.register(Emails)