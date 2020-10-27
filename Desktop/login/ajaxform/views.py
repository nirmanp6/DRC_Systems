from django.shortcuts import render
from .forms import form1
from .models import Users
from django.http import JsonResponse
# Create your views here.
from .models import Post
import json

def create_post(request):
    posts = Post.objects.all()
    response_data = {}
    print("request caught")
    if request.method == 'POST':
        print("request.post verified")
        print(request.body)
        print(request.POST)
        #data = json.loads(request.body)
        title = request.POST.get('title')
        description = request.POST.get('description')
        print(title)
        print("data cleaned")
        Post.objects.create(
            title = title,
            description = description,
            )
        print("object created")
        response_data['title'] = title
        response_data['description'] = description
        print("response registered sending")
        return JsonResponse(response_data)

    return render(request, 'create_post.html', {'posts':posts}) 

def formEP(request):
    if request.method == 'POST':
        #form = form1(request.POST)
        #if form.is_valid():
        email = request.POST.get("email")
        password = request.POST.get("password")
        Users.objects.create(email=email, password=password)
        
        return JsonResponse({"e":"User created!"})

    else:
        form = form1()
        return render(request, 'formEP.html', {'form':form})