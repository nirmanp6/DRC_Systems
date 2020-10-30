import django.dispatch

from django.db import models
from django.dispatch import Signal, receiver

# Create a custom signal
order_signal = Signal(providing_args=["context"])
product_signal = Signal(providing_args=["context"])
add_rem_signal = Signal(providing_args=["context"])
user_activity_signal = Signal(providing_args=["context"])

class Signals(object):
    # function to send the signal
    def product_send(self,**kwargs):
        s = kwargs['slug']
        a = kwargs['action']
        product_signal.send(sender=self.__class__,slug=s,action=a)

    def user_activity_send(self,email,action):
        e = email
        a = action
        user_activity_signal.send(sender=self.__class__,email=e, action=a)

# Function to receive the signal
@receiver(product_signal)
def product_receive(sender, **kwargs):
    s = kwargs['slug']
    a = kwargs['action']
    ProductSignal.objects.create(product_slug=s, action=a)

@receiver(user_activity_signal)
def user_activity_receive(sender, **kwargs):
    e = kwargs['email']
    a = kwargs['action']
    UserSignal.objects.create(email=e, action=a)

# Create your models here.

class UserSignal(models.Model):
    email = models.EmailField()
    action = models.CharField(max_length=200)
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        string = self.email + " " + self.action + " " + str(self.at)
        return string

class CartSignal(models.Model):
    cart_id = models.IntegerField()
    action = models.CharField(max_length=200)
    at = models.DateTimeField(auto_now_add=True)

class ProductSignal(models.Model):
    product_slug = models.SlugField()
    action = models.CharField(max_length=200)
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        string = self.product_slug + " " + self.action + " " + str(self.at)
        return string


