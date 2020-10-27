from django import forms
import phonenumbers
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib import messages
from django.shortcuts import render, redirect

class RegisterForm(forms.Form):
    """

    """
    email = forms.EmailField(
        label='email address',
        max_length=255)
    f_name = forms.CharField(max_length=30)
    country = CountryField().formfield()
    mobile = forms.CharField(max_length=16)
    address = forms.CharField(max_length=300)
    pwd1 = forms.CharField(label='Password:', max_length=32, widget=forms.PasswordInput)
    pwd2 = forms.CharField(label='Confirm Password', max_length=32, widget=forms.PasswordInput)

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.filter(email= data)
        if qs.exists():
            msg = "User with that email already exists"
            self.add_error('email',msg)
            #return redirect ('/fail/')
        return data