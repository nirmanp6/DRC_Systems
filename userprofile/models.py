import itertools
from django_countries.fields import CountryField

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    '''Profile model to store other data
    about user which is not email'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=17, blank=True)
    address = models.TextField(max_length=500, blank=True)
    country = CountryField()
    checkbox = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''receives signal of user create
    and creates profile related to it'''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    '''updates the profile model
    when user model is changed'''
    instance.profile.save()


class Emails(models.Model):
    '''model to store the alternate
    emails the user may decide to add'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email1 = models.EmailField(max_length=30, blank=True, null=True)
    email2 = models.EmailField(max_length=30, blank=True, null=True)
    email3 = models.EmailField(max_length=30, blank=True, null=True)
    email4 = models.EmailField(max_length=30, blank=True, null=True)
    email5 = models.EmailField(max_length=30, blank=True, null=True)
    add_email = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        if (self.email5 != None):
            self.add_email = False
        else:
            self.add_email = True
        super(Emails, self).save(*args, **kwargs)


'''same as above signals, makes sure
emails category is created/updated'''
@receiver(post_save, sender=User)
def create_user_email(sender, instance, created, **kwargs):
    if created:
        Emails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_email(sender, instance, **kwargs):
    instance.emails.save()
