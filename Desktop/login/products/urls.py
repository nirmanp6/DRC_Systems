from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import cartv


urlpatterns = [
    path('cart/', views.check_mt, name='cart'),
    path('cart/view/', cartv.as_view(), name='cartv'),
    path('order/', views.ordercart, name='ordercart'),
    path('cart_qt/', views.get_cart_qt, name='get_cart_qt'),
    path('', views.products.as_view(), name='home'),
    path('<slug:slug>/', views.productview),
    path('<slug:slug>/add/', views.add),
    path('<slug:slug>/rem/', views.rem),
]