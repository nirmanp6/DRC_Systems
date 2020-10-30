from django.shortcuts import render
from django.dispatch import receiver

from signals.models import ProductSignal, product_signal
# Create your views here.
@receiver(product_signal)
def product_signal_receive(sender, slug, action):
    s = slug
    a = action
    ProductSignal.objects.create(product_slug=s, action=a)