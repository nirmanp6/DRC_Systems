from django.urls import path, include

from .views import *

urlpatterns = [
    path('register/', register, name="signup"),
    path('login/', login1, name='login'),
    path('profile/', profile, name='profile'),
    path('fail/', failure, name='failure'),
    path('logout/', signout, name='logout'),
    path('register/1/', success, name='success'),
    path('add_email/', add_email, name='add_email'),
]