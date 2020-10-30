from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import cartv


urlpatterns = [
    path('cart/', cartv.as_view(), name='cart'),
    path('<slug:slug>/', views.productview),
    path('<slug:slug>/add/', views.add),
    path('<slug:slug>/rem/', views.rem),
]