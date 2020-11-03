# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pdb

from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from signals.models import Signals
from task1.tasks import order_email
from django.contrib.auth.models import User
from .models import product, cart, cart_item
# Create your views here.


class products(generic.ListView):
    '''extending generic list
    view to display all products
    pass queryset of all products
    as context to list view'''
    model = product
    context_object_name = 'product_list'
    queryset = product.objects.all()
    template_name = 'products/productsview.html'


def productview(request, **kwargs):
    '''detailed product view of single
    product, url is unique by slug'''
    # get slug from URL
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    context = {'product': product1}
    return render(request, 'productview.html', context)


@login_required()
def add(request, **kwargs):
    '''add to cart functionality handled completely by
    ajax still available via link calling, get product
    slug from the url, login required to add to cart'''
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    # DRY principle this code is called
    # in two different blocks

    def itemadd(request, **kwargs):
        # send signal to user and product db
        signal = Signals()
        slug = product1.slug
        email = request.user.email
        action = product1.name + " added to cart"
        signal.product_send(slug=slug, action=action)
        signal.user_activity_send(email=email, action=action)
        # check if cartitem for product exists
        qs = cart_item.objects.filter(
            user__email=request.user.email,
            products__slug=product1.slug,
            status="1"
        )
        if qs.exists():
            # if cart_item exists, update
            c = qs[0]
            c.quantity = c.quantity + 1
            c.totalprice += product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()

        else:
            # if cartitem doesn't exist, create
            c = cart_item.objects.create(quantity=1, user=request.user)
            c.products.add(product1)
            c.productname = product1.name
            c.productprice = product1.price
            c.totalprice += product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()
        # item_add func ends

    # check if user has cart
    cartqs = cart.objects.filter(
        user__email=request.user.email,
        status="1"
    )
    # if user has cart, update
    if cartqs.exists():
        itemadd(request)
        cart1 = cartqs[0]
        qs = cart_item.objects.filter(
            products__slug=product1.slug,
            user__email=request.user.email,
            status="1",
        )
        # if cart has cart_item, update cart
        if qs.exists():
            c = qs[0]
            cart1.items.add(c)
            cart1.total += product1.price
            cart1.total = round(cart1.total, 2)
            cart1.quantity += 1
            cart1.save()
        # if cart doesn't have cartitem, create it
        else:
            c = cart_item(
                quantity=1,
                productname=product1.name,
                productprice=product1.price
            )
            c.save()
            c.user.add(request.user)
            cart1.items.add(c)
            cart1.total += product1.price
            cart1.total = round(cart1.total, 2)
            cart1.quantity += 1
            c.save()
            cart1.save()

    # if user doesn't have cart create it
    else:
        itemadd(request)
        qs = cart_item.objects.filter(
            products__slug=product1.slug,
            user__email=request.user.email,
            status="1",
        )
        c = qs[0]
        cart1 = cart.objects.create(user=request.user)
        cart1.items.add(c)
        cart1.total += product1.price
        cart1.total = round(cart1.total, 2)
        cart1.quantity += 1
        cart1.save()
    # dynamically update the page by providing relevant data
    cart_data = get_cart_qt(request)
    qs = cart_item.objects.filter(
        user__email=request.user.email,
        products__slug=product1.slug,
        status="1"
    )
    c = qs[0]
    cart_data["item_qt"] = c.quantity
    cart_data["item_totprice"] = c.totalprice
    # doesn't return HTTPresponse beacuse
    # only ajax calls execute this view
    return JsonResponse(cart_data)


@login_required
def rem(request, **kwargs):
    '''remove from cart functionality gives error
    if unauthenticated user calls function, only
    ajax calls, doesn't give error is user doesn't
    have item in cart'''
    # get product slug from URL
    product1 = get_object_or_404(product, slug=kwargs.get('slug'))
    # senbd signal to user and product db
    signal = Signals()
    slug = product1.slug
    email = request.user.email
    action = product1.name + " removed from cart"
    signal.product_send(slug=slug, action=action)
    signal.user_activity_send(email=email, action=action)
    # check if cart_item for this product exist
    qs = cart_item.objects.filter(
        user__email=request.user.email,
        products__slug=product1.slug,
        status="1"
    )
    # if cartitem exists update and check
    # whether quantity=0 after removing
    if qs.exists():
        c = qs[0]
        # check if quantity=1 before removing
        if c.quantity == 1:
            c.quantity -= 1
            c.totalprice -= product1.price
            c.totalprice = round(c.totalprice, 2)
            qs = cart.objects.filter(
                user__email=request.user.email,
                status="1"
            )
            cart1 = qs[0]
            cart1.quantity -= 1
            cart1.total -= product1.price
            cart1.total = round(cart1.total, 2)
            cart1.items.remove(c)
            c.delete()
            cart1.save()
            # cartitem destroyed item no longer in cart
            return JsonResponse({"e": "Item removed from Cart"})
        # if quantity!=1 before removing do this
        else:
            c.quantity -= 1
            c.totalprice -= product1.price
            c.totalprice = round(c.totalprice, 2)
            c.save()
            # item removed
        # check if cart is empty or not
        qs = cart.objects.filter(
            user__email=request.user.email,
            status="1"
        )
        if qs.exists():
            cart1 = qs[0]
            cart1.total -= product1.price
            cart1.total = round(cart1.total, 2)
            cart1.quantity -= 1
            cart1.save()
            # check if cartquantity=0 if yes delete cart
            if cart1.quantity == 0:
                cart1.delete()
                return JsonResponse(
                    {"e": "All items removed from Cart"})
    # if item not in cart show error
    else:
        return JsonResponse({"e": "Product was not in your cart"}, status=500)
        messages.error(request, "Product was not in your cart")
        return redirect('failure')

    # send JsonResponse to dynamically update the page
    cart_data = get_cart_qt(request)
    qs = cart_item.objects.filter(
        user__email=request.user.email,
        products__slug=product1.slug,
        status="1"
    )
    c = qs[0]
    cart_data["item_qt"] = c.quantity
    cart_data["item_totprice"] = c.totalprice
    # only ajax calls to this view
    return JsonResponse(cart_data)


@login_required
def check_mt(request):
    # FBV to check whether cart is empty,
    # redirecting to CBV cartv cartview
    qs = cart.objects.filter(user__email=request.user.email, status="1")
    if qs.exists():
        cart1 = qs[0]
        qs = cart1.items.all()
        if qs.exists():
            return redirect("cartview")
        else:
            messages.error(request, "There are no items in your cart")
            return redirect("/fail/")

    else:
        messages.error(request, "There are no items in your cart")
        return redirect("/fail/")


class cartv(generic.ListView):
    '''generic listview to display cart'''

    def no_login_redir(self):
        # check if suer is logged in or not
        if not self.request.user.is_authenticated:
            # redirect away if not logged in
            return redirect('login')
    model = cart_item
    context_object_name = 'cart_list'

    def get_queryset(self):
        # pass context to generic list view
        qs = cart.objects.filter(
            user__email=self.request.user.email, status="1")
        c = qs[0]
        return c.items.all()
    template_name = 'products/cartview.html'

    def get_context_data(self, **kwargs):
        # provide additional data using this
        context = super(cartv, self).get_context_data(**kwargs)
        context['total'] = cart.objects.filter(
            user__email=self.request.user.email, status="1")
        return context


def ordercart(request, **kwargs):
    '''order cart using ajax call
    checks whetehr cart exists 
    and if it's empty or not '''
    # non authenticated user can't access
    if not request.user.is_authenticated:
        return redirect('login')
    cartqs = cart.objects.filter(user__email=request.user.email, status="1")
    # check if user has active cart or not
    if cartqs.exists():
        tempc = cartqs[0]
        qs = tempc.items.all()
        # check if cart has items or not
        if qs.exists():
            # chenge cart status to ordered
            c = cartqs[0]
            c.status = "2"
            c.ordered_date = timezone.now()
            c.save()
            # cahnge status of related
            # cartitems to ordered
            for cart_item in c.items.all():
                cart_item.status = "2"
                cart_item.save()
            # send signal to user db
            email = request.user.email
            action = "Order Placed"
            signal = Signals()
            signal.user_activity_send(email, action)
            # send email to user about purchase
            cust_email = request.user.email
            message = order_m(c)
            order_email.delay(cust_email, message)
            return JsonResponse({'e': "Order was placed"})
        else:
            return redirect('/fail/')

    else:
        return redirect('/fail/')


class orderv(generic.ListView):
    # dashboard generic listview to display all orders
    # redirect if user not authenticated
    def no_login_redir(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
    model = cart_item
    context_object_name = 'order_list'
    # sned queryset of all orders to listview

    def get_queryset(self):
        qs = cart.objects.filter(
            user__email=self.request.user.email,
            status="2").order_by('-ordered_date')
        return qs
    template_name = 'products/orderview.html'
    # provide additional data

    def get_context_data(self, **kwargs):
        context = super(orderv, self).get_context_data(**kwargs)
        context['total'] = cart.objects.filter(
            user__email=self.request.user.email,
            status="2").order_by('-ordered_date')
        return context


def get_cart_qt(request):
    '''DRY: use this function when updating cart
    to dynamically update cart quantity on page'''
    qs = cart.objects.filter(
        user__email=request.user.email,
        status="1",
    )
    c = qs[0]
    qt = c.quantity
    total = c.total
    cart_data = {"qt": qt, "total": total}
    # convert this dict to JSON in the view it's called
    return cart_data


def order_m(c):
    '''DRY: use this function to send
    mail to the user after purchase'''
    s = "\n"
    n = 1
    # add all cartitems to list
    for cart_item in c.items.all():
        s += str(n)+") " + cart_item.productname + " : \t\t" +\
            str(cart_item.productprice) + \
            " x " + str(cart_item.quantity) + " for " + \
            str(cart_item.totalprice) + "\n"
        n += 1
    # add all relevant details together
    message = "You recently placed an order for \n" + \
        s + "\nTotal: " + str(c.total) + "\n\nThank you!"
    # final mail to be sent by the celery worker
    return message
