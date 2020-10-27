from django.urls import path
from .views import formEP, create_post
urlpatterns = [
    path('', formEP, name="login"),
]