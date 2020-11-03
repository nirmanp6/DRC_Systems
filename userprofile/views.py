from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from signals.models import Signals
from .models import Profile, Emails
from .forms import RegisterForm, EmailForm
# Create your views here.


def register(request):
    ''' register user using django form, check
     if user is logged in, redirect if yes '''
    if request.user.is_authenticated:
        return redirect('home')
    # if method is POST, get data from form and create user
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # run validations before creating user
        if form.is_valid():
            pwd = form.cleaned_data['pwd1']
            pwd2 = form.cleaned_data['pwd2']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            full_name = form.cleaned_data['f_name']
            username = form.cleaned_data['username']
            messages.success(request, 'User Created')
            user = User.objects.create(
                username=username,
                email=email,
            )
            user.set_password(pwd)
            user.save()
            '''Profile has one-to-one link with user
            save login credentials in user, other data
            in profile'''
            Profile.objects.filter(user=user).update(
                full_name=full_name, mobile=mobile,
                country=country, address=address)
            # send user created signal
            signal = Signals()
            e = email
            a = "account created"
            signal.user_activity_send(email=e, action=a)
            return redirect('profile')
        else:
            '''if validations fail return user 
            to bound form and display errors'''
            form = RegisterForm(request.POST)
            return render(request, 'register.html', {'form': form})

    # if method is GET render form page
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def login1(request):
    ''' login and authenticate user, check if
    user has already logged in to prevent error'''
    if request.user.is_authenticated:
        return redirect('profile')
    # if method is POST fetch data and authenticate
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        ''' to use default django user model
        we have to login with username so query
        user db with email and fetch username'''
        qs = User.objects.filter(email=email)
        if qs.exists():
            userem = qs[0]
            username = userem.username
        user = authenticate(username=username, password=pwd)
        # default django authenticate function
        if user is not None:
            login(request, user)
            return JsonResponse({"s": 1, "e": "User authenticated"})
        # if authentication fails display error
        else:
            qs = User.objects.filter(email=email)
            if qs.exists():
                # user with email exists but pwd doesn't match
                return JsonResponse(
                    {"s": "pwd", "e": "The password is incorrect"}, status=500)
            else:
                # user with email doesn't exist
                return JsonResponse(
                    {"s": "email",
                     "e": "No user is registered with that email"}, status=500)

    else:
        # if method is POST render login page
        return render(request, 'login.html')


@login_required
def profile(request):
    '''profile page to display data 
    from all three related tables
    User, Profile and Emails'''
    return render(request, 'profile.html', {'user': request.user})
    # profile doesn't have a form to edit data yet


@login_required
def signout(request):
    '''signout logged in user
    using default django auth'''
    # send user logout signal
    signal = Signals()
    e = request.user.email
    a = "logged out"
    signal.user_activity_send(email=e, action=a)
    logout(request)
    return redirect('login')


def success(request):
    '''placeholder page to 
    display success message'''
    return render(request, 'success.html')


def failure(request):
    '''redirect user to this page in case 
    of error, displays error message'''
    return render(request, 'failure.html')


def dash(request):
    ''' FBV to check whether user is
    logged in before redirecting to 
    CBV dash which displays orders'''
    if request.user.is_authenticated:
        return redirect('orderv')

    else:
        return redirect('login')


@login_required
def add_email(request):
    ''' Form page to allow user to add five
     alternate emails to Emails model '''
    saved_emails = request.user.emails
    # if method is POST use modelForm with instance
    # to show saved emails and allow to add more
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=saved_emails)
        if form.is_valid():
            email1 = form.cleaned_data['email1']
            email2 = form.cleaned_data['email2']
            email3 = form.cleaned_data['email3']
            email4 = form.cleaned_data['email4']
            email5 = form.cleaned_data['email5']
            saved_emails.save()
            return redirect('profile')
    # if method is POST render form page
    else:
        form = EmailForm(instance=saved_emails)
        return render(request, 'add_email.html', {'form': form})
