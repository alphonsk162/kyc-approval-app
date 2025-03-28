from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .helper_functions import validate, find_submitted_requests
from .models import Citizen
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_signup(request):
    return render(request, "user_signup.html")

def user_login(request):
    return render(request, "user_login.html")

def register_user(request):
    if request.POST:
        full_name = request.POST.get('fullname')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        email_id = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        password_copy = request.POST.get('confirm_password')
        if validate(request, password, password_copy, email_id, phone_number) == False:
            return redirect("user_signup")
        else:
            user = User.objects.create(username=email_id, password=make_password(password), email=email_id)
            citizen = Citizen.objects.create(user=user, full_name=full_name, dob=dob, address=address, phone_number=phone_number[::-1][:10][::-1], gender=gender)
    return render(request, 'user_signup.html')

@login_required(login_url="user_login")
def user_home_page(request):
    user = request.user
    citizen_obj = Citizen.objects.get(user=user)
    requests = list(find_submitted_requests(request.user))
    print(requests)
    context = {'fullname': citizen_obj.full_name,
                'email': user.email, 'requests': requests}
    return render(request, 'user_home_page.html', context)

def user_signin(request):
    if request.POST.get("email"):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("user_home_page")
        else:
            messages.error(request, "Invalid email id or password")
            return redirect("user_login")

    elif request.POST.get("mobile"):
        phone_number = request.POST.get("mobile")
        citizen_obj = Citizen.objects.filter(phone_number=phone_number).first()
        if citizen_obj:
            user_obj = citizen_obj.user
            username = user_obj.username
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("user_home_page")
        else:
            messages.error(request, "Invalid phone number or password")
            return redirect("user_login")

def user_signout(request):
    logout(request)
    return redirect("user_login")










