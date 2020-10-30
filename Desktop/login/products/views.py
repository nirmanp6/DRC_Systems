# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from .models import product, cart, cart_item
from accounts.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from login.tasks import order_email, my_first_task
import json, pdb
# Create your views here.
class FailedJsonResponse(JsonResponse):
    def __init__(self, data):
        super().__init__(data)
        self.status_code = 400

class products(generic.ListView):
    model = product
    context_object_name = 'product_list'   
    queryset = product.objects.all()
    template_name = 'products/productsview.html'

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productview(request, **kwargs):
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    context={
    'product': product1
    }
    return render(request, 'productview.html',context)

@login_required()
def add(request, **kwargs):
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))

    def itemadd(request, **kwargs):
        qs = cart_item.objects.filter(
                user__email=request.user.email,
                products__slug=product1.slug,
                status = "1"
                )
        if qs.exists():
            
            c = qs[0]
            c.quantity = c.quantity + 1
            c.totalprice += product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()

        else:
            print("cartitemcreate")
            c = cart_item.objects.create(quantity=1)
            c.save()
            c.user.add(request.user)
            c.products.add(product1)
            c.productname = product1.name
            c.productprice = product1.price
            c.totalprice += product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()

    cartqs = cart.objects.filter(
            user__email=request.user.email,
            status = "1"
            )
    if cartqs.exists():
        itemadd(request)
        
        cart1 = cartqs[0]
        qs = cart_item.objects.filter(
            products__slug=product1.slug,
            user__email=request.user.email,
            status = "1",
            )
        if qs.exists():
            c = qs[0]
            print(str(c))
            cart1.items.add(c)
            cart1.total += product1.price
            cart1.total = round(cart1.total, 2)
            cart1.quantity += 1
            cart1.save()
        else:
            c = cart_item(
                quantity=1,
                productname=product1.name,
                productprice=product1.price
                )
            c.save()
            a=request.user
            c.user.add(a)
            cart1.items.add(c)
            cart1.total += product1.price
            cart1.total = round(cart1.total, 2)
            cart1.quantity += 1
            c.save()
            cart1.save()

    else:
        print("cartcreate")
        itemadd(request)
        qs = cart_item.objects.filter(
            products__slug=product1.slug,
            user__email=request.user.email,
            status = "1",
            )
        c = qs[0]
        cart1 = cart.objects.create(user = request.user)
        cart1.items.add(c)
        cart1.total += product1.price
        cart1.total = round(cart1.total, 2)
        cart1.quantity += 1
        cart1.save()
    cart_data = get_cart_qt(request)
    qs = cart_item.objects.filter(
                user__email=request.user.email,
                products__slug=product1.slug,
                status = "1"
                )
    c=qs[0]
    cart_data["item_qt"] = c.quantity
    cart_data["item_totprice"] = c.totalprice
    return JsonResponse(cart_data)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def rem(request, **kwargs):

    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    qs = cart_item.objects.filter(
            user__email=request.user.email,
            products__slug=product1.slug,
            status = "1"
            )
    if qs.exists():
        c = qs[0]
        if c.quantity == 1:
            print("quantity=1")
            c.quantity-=1
            c.totalprice -= product1.price
            c.totalprice = round(c.totalprice, 2)
            qs = cart.objects.filter(
                    user__email=request.user.email,
                    status = "1"
                 )
            cart1=qs[0]
            cart1.quantity -= 1
            cart1.total -= product1.price
            cart1.total = round(cart1.total, 2)
            cart1.items.remove(c)
            c.delete()
            cart1.save()
            return FailedJsonResponse({"e": "Item removed from Cart"})
        else:
            c.quantity-=1
            c.totalprice -= product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()
            qs = cart.objects.filter(
                 user__email=request.user.email,
                 status = "1"
                 )
            if qs.exists():
                cart1 = qs[0]
                cart1.total -= product1.price
                cart1.total = round(cart1.total, 2)
                cart1.quantity -= 1
                cart1.save()
                if cart1.quantity == 0:
                    return FailedJsonResponse({"e": "All items removed from Cart"})
    else:
        return FailedJsonResponse({"e": "Product was not in your cart"})
        messages.error(request,"Product was not in your cart")
        return redirect('failure')

    cart_data = get_cart_qt(request)
    qs = cart_item.objects.filter(
                user__email=request.user.email,
                products__slug=product1.slug,
                status = "1"
                )
    c=qs[0]
    cart_data["item_qt"] = c.quantity
    cart_data["item_totprice"] = c.totalprice
    return JsonResponse(cart_data)    


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def check_mt(request):
    qs = cart.objects.filter(user__email=request.user.email, status="1")
    cart1 = qs[0]
    qs = cart1.items.all()
    if qs.exists():
        return redirect("cartv")
    else:
        messages.error(request, "There are no items in your cart")
        return redirect("/fail/")

class cartv(generic.ListView):
    def no_login_redir(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
    model = cart_item
    context_object_name = 'cart_list'   
    def check_mt(self):
        qs = cart.objects.filter(user__email=self.request.user.email, status="1")
        if qs.exists():
            return redirect("cartv")
        else:
            messages.error(request, "There are no items in your cart")
            return redirect("/fail/")

    def get_queryset(self):
        qs = cart.objects.filter(user__email=self.request.user.email, status="1")
        c = qs[0]
        return c.items.all()
    template_name='products/cartview.html'

    def get_context_data(self, **kwargs):
        context = super(cartv, self).get_context_data(**kwargs)
        context['total'] = cart.objects.filter(user__email=self.request.user.email, status="1") 
        return context
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ordercart(request, **kwargs):
    
    if not request.user.is_authenticated:
        return redirect('login')
    cartqs = cart.objects.filter(user__email = request.user.email, status="1")
    if cartqs.exists():
        tempc = cartqs[0]
        qs = tempc.items.all()
        if qs.exists():
            c = cartqs[0]
            c.status = "2"
            c.ordered_date = timezone.now()
            c.save()
            for cart_item in c.items.all():
                cart_item.status = "2"
                cart_item.save()
            cust_email = request.user.email
            message = order_m(c)
            order_email.delay(cust_email, message)
            print("ordered")
            return JsonResponse({'e': "Order was placed"})

    else:
        return redirect('/fail/')


class orderv(generic.ListView):
    def no_login_redir(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
    model = cart_item
    context_object_name = 'order_list'   
    

    def get_queryset(self):
        qs = cart.objects.filter(user__email=self.request.user.email, status="2").order_by('-ordered_date')
        return qs
    template_name='products/orderview.html'

    def get_context_data(self, **kwargs):
        context = super(orderv, self).get_context_data(**kwargs)
        context['total'] = cart.objects.filter(user__email=self.request.user.email, status="2").order_by('-ordered_date')
        return context

def get_cart_qt(request):
    qs = cart.objects.filter(
        user__email = request.user.email,
        status = "1",
        )
    c = qs[0]
    qt = c.quantity
    total = c.total
    cart_data = {"qt": qt, "total": total}
    return cart_data


def order_m(c):
    s = "\n"
    n = 1
    for cart_item in c.items.all():
        s += str(n)+") " + cart_item.productname + " : \t\t" + str(cart_item.productprice) + " x " + str(cart_item.quantity) + " for " +str(cart_item.totalprice) + "\n"
        n += 1
    message = "You recently placed an order for \n" + s + "\nTotal: " + str(c.total) + "\n\nThank you!"
    return message