from django.shortcuts import render, redirect
from .models import Officer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# Create your views here.

def officer_login(request):
    return render(request, 'officer_login.html')

def officer_signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        officer_obj = Officer.objects.get(username=username)
    except Officer.DoesNotExist:
        officer_obj = None
        messages.error(request, "Invalid Username or password")
        return redirect('officer_login')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("officer_home_page")
    else:
        messages.error(request, "Invalid email id or password")
        return redirect("officer_login")

@login_required(login_url="officer_login")
def officer_home_page(request):
    return render(request, 'officer_home_page.html')