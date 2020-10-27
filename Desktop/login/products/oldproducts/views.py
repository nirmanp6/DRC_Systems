# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import ListView
from .models import product, cart, cart_item
from accounts.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

class home(generic.ListView):
    model = product
    context_object_name = 'product_list'   
    queryset = product.objects.all()
    template_name = 'products/home.html'


def productview(request, **kwargs):
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    return render(request, 'productview.html',{'product':product1})

@login_required()
def add(request, **kwargs):
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    if cart_item.objects.filter(user__email=request.user.email,products__slug=kwargs.get('slug')).exists():
            qs = cart_item.objects.filter(user__email=request.user.email,products__slug=kwargs.get('slug'))
            c = qs[0]
            c.quantity = c.quantity + 1
            c.totalprice += product1.price
            c.save()

    else:
        c = cart_item.objects.create(quantity=1)
        c.save()
        c.user.add(request.user)
        c.products.add(product1)
        c.productname = product1.name
        c.productprice = product1.price
        c.totalprice += product1.price
        c.save()

    if cart.objects.filter(user__email=request.user.email).exists():
        qs = cart.objects.filter(user__email=request.user.email)
        cart1 = qs[0]
        qs = cart_item.objects.filter(products__slug=kwargs.get('slug'),user__email=request.user.email)
        if qs.exists():
            c = qs[0]
            cart1.items.add(c)
            cart1.total += product1.price
            cart1.save()
        else:
            c = cart_item(quantity=1, productname=product1.name, productprice=product1.price)
            c.save()
            a=request.user
            c.user.add(a)
            cart1.items.add(c)
            cart1.total += product1.price
            c.save()
            cart1.save()

    else:
        qs = cart_item.objects.filter(products__slug=kwargs.get('slug'))
        c = qs[0]
        cart1 = cart.objects.create(ordered=False, user = request.user)
        cart1.items.add(c)
        cart1.total += product1.price
        cart1.save()

    return redirect('home')


@login_required
def rem(request, **kwargs):
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    if cart_item.objects.filter(user__email=request.user.email,products__slug=kwargs.get('slug')).exists():
            qs = cart_item.objects.filter(user__email=request.user.email,products__slug=kwargs.get('slug'))
            c = qs[0]
            c.quantity-=1
            c.totalprice -= product1.price
            if c.quantity == 0:
                qs= cart_item.objects.filter(products__slug=kwargs.get('slug'),
                        user__email=request.user.email)
                c = qs[0]
                c.delete()
                qs = cart.objects.filter(products__slug=kwargs.get('slug'),
                    user__email=request.user.email)
                cart1 = qs[0]
                cart1.total -= product1.price
                cart1.save()
                return redirect('home')
            c.save()
    else:
        return redirect('failure')

    if cart.objects.filter(user__email=request.user.email).exists():
        qs = cart.objects.filter(user__email=request.user.email)
        cart1 = qs[0]
        cart1.items.add(c)
        cart1.total -= product1.price
        cart1.save()
        


    return redirect('home')



class cartv(generic.ListView):
    model = cart_item
    context_object_name = 'cart_list'   
    def get_queryset(self):
        qs = cart.objects.filter(user__email=self.request.user.email)
        c = qs[0]
        return c.items.all()
    template_name='products/cartview.html'

    def get_context_data(self, **kwargs):
        context = super(cartv, self).get_context_data(**kwargs)
        context['total'] = cart.objects.filter(user__email=self.request.user.email) 
        return context


'''
def cartv(request, **kwargs):
    qs = cart.objects.filter(user__email=request.user.email)
    c = qs[0]
    return render(request, 'cartview.html',{'c':c})
'''

