from django.shortcuts import render, redirect
from .models import Citizen
from kyc_approval_app.models import KYCRequest
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .helper_functions import validate, find_submitted_requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from officer.models import Officer
from django.http import HttpResponseForbidden
# Create your views here.

def user_signup(request):
    if request.user.is_authenticated:
        # try:
        #     officer_obj = Officer.objects.get(user=request.user)
        #     return redirect("officer_home_page")
        # except Officer.DoesNotExist:
        #     return redirect("user_home_page")
        logout(request)
    return render(request, "user_signup.html")

def user_login(request):
    if request.user.is_authenticated:
        # try:
        #     officer_obj = Officer.objects.get(user=request.user)
        #     return redirect("officer_home_page")
        # except Officer.DoesNotExist:
        #     return redirect("user_home_page")
        logout(request)
    return render(request, "user_login.html")

def register_user(request):
    if request.POST:
        full_name = request.POST.get("fullname")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone")
        email_id = request.POST.get("email")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        password_copy = request.POST.get("confirm_password")
        if validate(request, password, password_copy, email_id, phone_number) == False:
            return redirect("user_signup")
        else:
            user = User.objects.create(
                username=email_id, password=make_password(password), email=email_id
            )
            citizen = Citizen.objects.create(
                user=user,
                full_name=full_name,
                dob=dob,
                address=address,
                phone_number=phone_number,
                gender=gender,
            )
    return render(request, "user_signup.html")

def user_home_page(request):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        user = request.user
        citizen_obj = Citizen.objects.get(user=user)
        requests = list(find_submitted_requests(request.user))
        context = {
            "fullname": citizen_obj.full_name,
            "email": user.email,
            "requests": requests,
        }
        return render(request, "user_home_page.html", context)

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
    return redirect("kyc_app")

def request_kyc_approval(request):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        full_name = citizen_obj.full_name
        dob = citizen_obj.dob
        gender = citizen_obj.gender
        address = citizen_obj.address
        phone = citizen_obj.phone_number
        context = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "address": address,
            "phone": phone,
            "email": request.user.email,
        }
        return render(request, "kyc_request_form.html", context)


def submit_request(request):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        id_proof_name = request.POST.get("id_proof_name")
        address_proof_name = request.POST.get("address_proof_name")
        id_proof_file = request.FILES["id_proof_file"]
        address_proof_file = request.FILES["address_proof_file"]
        new_request = KYCRequest.objects.create(
            citizen=citizen_obj,
            id_proof_name=id_proof_name,
            address_proof_name=address_proof_name,
            id_proof_file=id_proof_file,
            address_proof_file=address_proof_file,
        )
        new_request.request_id = (
            "KYC-" + timezone.now().strftime("%d-%m-%Y") + "-" + str(new_request.id)
        )
        new_request.save()
        return redirect("user_home_page")


def edit_profile(request):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        full_name = citizen_obj.full_name
        dob = citizen_obj.dob
        gender = citizen_obj.gender
        address = citizen_obj.address
        phone = citizen_obj.phone_number
        context = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "address": address,
            "phone": phone,
            "email": request.user.email,
        }
        return render(request, "edit_profile.html", context)


def update_profile(request):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        full_name = request.POST.get("full_name")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        email_id = request.POST.get("email")
        gender = request.POST.get("gender")
        request.user.username = email_id
        request.user.email = email_id
        request.user.save()
        citizen_obj.full_name = full_name
        citizen_obj.dob = dob
        citizen_obj.address = address
        citizen_obj.phone_number = phone_number
        citizen_obj.gender = gender
        citizen_obj.save()
        return redirect("edit_profile")


def edit_submission(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        kyc_request = KYCRequest.objects.get(id=id)
        citizen_obj = Citizen.objects.get(user=request.user)
        if kyc_request.citizen != citizen_obj:
            return HttpResponseForbidden("You are not allowed to view this request.")
        full_name = citizen_obj.full_name
        dob = citizen_obj.dob
        gender = citizen_obj.gender
        address = citizen_obj.address
        phone = citizen_obj.phone_number
        context = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "address": address,
            "phone": phone,
            "email": request.user.email,
            "kyc_request": kyc_request,
        }
        return render(request, "edit_submission.html", context)


def update_kyc_request(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
        logout(request)
        return redirect('kyc_app')
    except Officer.DoesNotExist:
        kyc_request = KYCRequest.objects.get(id=id)
        id_proof_name = request.POST.get("id_proof_name")
        address_proof_name = request.POST.get("address_proof_name")
        if request.FILES.get("id_proof_file"):
            kyc_request.id_proof_file = request.FILES["id_proof_file"]
        if request.FILES.get("address_proof_file"):
            kyc_request.address_proof_file = request.FILES["address_proof_file"]
        kyc_request.status = "pending"
        kyc_request.submitted_at = timezone.now()
        kyc_request.reviewed_at = None
        kyc_request.remarks = None
        kyc_request.id_proof_name = id_proof_name
        kyc_request.address_proof_name = address_proof_name
        kyc_request.save()
        return redirect("edit_submission", id=id)
