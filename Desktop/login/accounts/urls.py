from django.urls import path, include
from django.contrib import admin
from accounts.views import *

urlpatterns = [
    #path('registerview/', registerview.as_view(), name='registerview'),
    path('register/', register, name='register'),
    path('register/1/', success, name='success'),
    path('log/', logmein, name='logmein'),
    path('login/', login1, name='login'),
    path('fail/', failure, name='failure'),
    path('logout/', signout, name='logout')

]