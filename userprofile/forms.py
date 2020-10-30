import re

from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import User, Emails

class RegisterForm(forms.Form):
    ''' Form to get user details required to register
        this specific form fills up Profile model '''
    email = forms.EmailField(
        label='email address',
        max_length=255)
    username = forms.CharField(max_length=20)
    full_name = forms.CharField(max_length=30)
    country = CountryField().formfield()
    mobile = forms.CharField(max_length=16)
    address = forms.CharField(max_length=300)
    pwd1 = forms.CharField(label='Password:', max_length=32, widget=forms.PasswordInput)
    pwd2 = forms.CharField(label='Confirm Password', max_length=32, widget=forms.PasswordInput)

    def clean_email(self):
        '''form validation, check if email is
        in valid format or not and see if email
        is associated with another user or not'''
        data = self.cleaned_data['email']
        qs = User.objects.filter(email= data)

        if qs.exists():
            msg = "User with that email already exists"
            self.add_error('email', msg)
            #return redirect ('/fail/')
        if not(re.match(r'^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z])+$)',data)):
            msg = "Please enter valid email"
            self.add_error('email', msg)
        return data


    def clean_address(self):
        ''' CHeck whether email is entered or not'''
        data = self.cleaned_data['address']

        if (data == ""):
            msg = "Address cannot be empty"
            self.add_error('address', msg)

        return data

    def clean_f_name(self):
        '''check if fullname only has letters,is
        not empty and is lower than max_length'''
        data = self.cleaned_data['f_name']

        if (len(data)>30):
            msg = "Name is too big"
            self.add_error('f_name', msg)

        if not (re.match(r'[a-zA-Z\s]+$', data)):
            msg = "Please enter your name using regular letters"
            self.add_error('f_name', msg)

        if (data == ""):
            msg = "Name cannot be empty"
            self.add_error('f_name', msg)

        return data

    def clean_mobile(self):
        '''check if mobile number is
         in proper format or not'''
        data = self.cleaned_data['mobile']

        if not (re.match(r'^(\+|\d)[0-9]{7,15}$', data)):
            msg = "Mobile number is not valid"
            self.add_error('mobile', msg)

        return data

    def clean_pwd1(self):
        '''check if password 
        is entered or not'''
        data = self.cleaned_data['pwd1']

        if (data == ""):
              msg = "Password cannot be empty"
              self.add_error('pwd1', msg)

        return data

    def clean_pwd2(self):
        '''check whether user has
        enetered confirm password
        and it matches pwd'''
        data = self.cleaned_data
        pwd1 = data['pwd1']
        pwd2 = data['pwd2']

        if(pwd2 == ""):
             msg = "Please Confirm Password"
             self.add_error('pwd2', msg)

        if (pwd1 != pwd2):
            msg = "Passwords do not match"
            self.add_error('pwd2', msg)

        return data


class EmailForm(ModelForm):
    ''' Email form to display alternate
    emails of user and to update them
    or add more'''
    class Meta:
        model = Emails
        fields =['email1','email2','email3','email4','email5',]