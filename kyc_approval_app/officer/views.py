from django.shortcuts import render, redirect
from .models import Officer, RejectedRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from user.models import KYCRequest
from django.utils import timezone
from .helper_functions import send_status_email

# Create your views here.


def officer_login(request):
    return render(request, "officer_login.html")


def officer_signin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    try:
        officer_obj = Officer.objects.get(username=username)
    except Officer.DoesNotExist:
        officer_obj = None
        messages.error(request, "Invalid Username or password")
        return redirect("officer_login")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("officer_home_page")
    else:
        messages.error(request, "Invalid email id or password")
        return redirect("officer_login")


@login_required(login_url="officer_login")
def officer_home_page(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
    pending_requests = list(KYCRequest.objects.filter(status="pending"))
    officer_name = request.user.username
    context = {"officer_name": officer_name, "pending_requests": pending_requests}
    return render(request, "officer_home_page.html", context)


@login_required(login_url="officer_login")
def view_request(request, id):
    request_obj = KYCRequest.objects.get(id=id)
    context = {"request_obj": request_obj}
    return render(request, "view_request.html", context)


@login_required(login_url="officer_login")
def approve_request(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
    request_obj = KYCRequest.objects.get(id=id)
    request_obj.reviewed_at = timezone.now()
    request_obj.reviewed_by = officer.user
    request_obj.status = "approved"
    if request.POST.get("remarks"):
        request_obj.remarks = request.POST.get("remarks")
    request_obj.request_full_name = request_obj.citizen.full_name
    request_obj.request_dob = request_obj.citizen.dob
    request_obj.request_email = request_obj.citizen.user.email
    request_obj.request_phone_number = request_obj.citizen.phone_number
    request_obj.request_address = request_obj.citizen.address
    request_obj.request_gender = request_obj.citizen.gender
    request_obj.save()
    send_status_email(request_obj.citizen.user.email, request_obj)
    return redirect("officer_home_page")


@login_required(login_url="officer_login")
def reject_request(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
    request_obj = KYCRequest.objects.get(id=id)
    request_obj.status = "rejected"
    remarks = request.POST.get("remarks")
    request_obj.remarks = remarks
    request_obj.reviewed_by = request.user
    request_obj.reviewed_at = timezone.now()
    request_obj.save()
    RejectedRequest.objects.create(
        request_obj=request_obj,
        request_full_name=request_obj.citizen.full_name,
        request_dob=request_obj.citizen.dob,
        request_address=request_obj.citizen.address,
        request_gender=request_obj.citizen.gender,
        request_phone_number=request_obj.citizen.phone_number,
        request_email=request_obj.citizen.user.email,
        reviewed_by=request_obj.reviewed_by,
        id_proof_name=request_obj.id_proof_name,
        address_proof_name=request_obj.address_proof_name,
        submitted_at=request_obj.submitted_at,
        remarks=request_obj.remarks,
        id_proof_file=request_obj.id_proof_file,
        address_proof_file=request_obj.address_proof_file,
    )
    try:
        send_status_email(request_obj.citizen.user.email, request_obj)
        return redirect("officer_home_page")
    except Exception as e:
        return redirect("officer_home_page")


@login_required(login_url="officer_login")
def approved_requests(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
    approved_requests = KYCRequest.objects.filter(
        status="approved", reviewed_by=officer.user
    ).order_by("-reviewed_at")
    return render(
        request,
        "list_requests.html",
        {"requests": approved_requests, "status": "approved"},
    )


@login_required(login_url="officer_login")
def rejected_requests(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
    rejected_requests = KYCRequest.objects.filter(
        status="rejected", reviewed_by=officer.user
    ).order_by("-reviewed_at")
    return render(
        request,
        "list_requests.html",
        {"requests": rejected_requests, "status": "rejected"},
    )
