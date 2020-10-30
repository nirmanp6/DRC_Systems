from django.shortcuts import render, redirect
from . models import User, UserManager
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from login.tasks import my_first_task
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.cache import cache
import json
'''
class FailedJsonResponse(JsonResponse):
    def __init__(self, data):
        super().__init__(data)
        self.status_code = 400
'''
def dash(request):
    if request.user.is_authenticated:
        return redirect('orderv')

    else:
        return redirect('login')

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            f_name = form.cleaned_data['f_name']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['pwd1']
            pwd2 = form.cleaned_data['pwd2']
            messages.success(request, 'User Created')
            user = User.objects.create(
                    email=email, f_name=f_name, address= address,
                    country= country, mobile= mobile,
                    )
            user.set_password(password)
            user.save()
            print(form.errors)
            
            return redirect('/accounts/login/')
        
        else:
            print (form.errors)
            form = RegisterForm(request.POST)
            return render(request,'register.html', {'form':form})
            '''
            pwd1 = form.cleaned_data['pwd1']
            pwd2 = form.cleaned_data['pwd2']
            if pwd1!= pwd2:
                messages.error(request, 'Passwords do not match try again')
                return redirect('register')
            '''
    

    else:
        storage = messages.get_messages(request)
        for _ in storage:
            pass

        for _ in list(storage._loaded_messages):
            del storage._loaded_messages[0]
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})


def login1(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        user = authenticate(email=email, password=pwd)
        if user is not None:
            login(request, user)         
            return JsonResponse({"s":1,"e": "User authenticated"})
        else:
            qs = User.objects.filter(email=email)
            if qs.exists():
                return JsonResponse({"s":"pwd","e": "The password is incorrect"})
            else:
                return JsonResponse({"s":"email","e": "No user is registered with that email"})
    else:
        return render(request, 'login.html') 

@login_required
def signout(request):
    logout(request)
    cache.clear()
    return redirect ('login')

def success(request):
	print('success')
	return render(request, 'success.html')

def failure(request):
	return render(request, 'failure.html')

def logmein(request):
   email= request.GET.get('email')
   password = request.GET.get('pwd')
   user = authenticate(email=email, password=password)
   if user is not None:
       login(request, user)
       return HttpResponse('fine')
       
   else:
       return HttpResponse('bad')