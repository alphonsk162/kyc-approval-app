from django.shortcuts import render, redirect
from kyc_approval_app.models import RejectedRequest, KYCRequest
from .models import Officer
from user.models import Citizen
from kyc_approval_app.models import KYCRequest
from django.utils import timezone
from .helper_functions import send_status_email
from django.db.models import Q
from .tasks import send_kyc_status_email_task
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.

def officer_login(request):
    if request.user.is_authenticated:
        try:
            officer_obj = Officer.objects.get(user=request.user)
            return redirect("officer_home_page")
        except Officer.DoesNotExist:
            return redirect("user_home_page")
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


def officer_home_page(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
    pending_requests = list(KYCRequest.objects.filter(status="pending"))
    officer_name = request.user.username
    context = {"officer_name": officer_name, "pending_requests": pending_requests}
    return render(request, "officer_home_page.html", context)



def view_request(request, id):
    request_obj = KYCRequest.objects.get(id=id)
    try:
        officer = Officer.objects.get(user=request.user)
        context = {"request_obj": request_obj}
        return render(request, "view_request.html", context)
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        if request_obj.citizen != citizen_obj:
            return HttpResponseForbidden("You are not allowed to view this request.")
        context = {"request_obj": request_obj}
        return render(request, "view_request.html", context)



def approve_request(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
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
    # send_status_email(request_obj.citizen.user.email, request_obj)
    send_kyc_status_email_task.delay(request_obj.citizen.user.email, id)
    return redirect("officer_home_page")



def reject_request(request, id):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
    request_obj = KYCRequest.objects.get(id=id)
    request_obj.status = "rejected"
    remarks = request.POST.get("remarks")
    request_obj.remarks = remarks
    request_obj.reviewed_by = request.user
    request_obj.reviewed_at = timezone.now()
    request_obj.request_full_name = request_obj.citizen.full_name
    request_obj.request_email = request_obj.citizen.user.email
    request_obj.request_dob = request_obj.citizen.dob
    request_obj.request_address = request_obj.citizen.address
    request_obj.request_phone_number = request_obj.citizen.phone_number
    request_obj.request_gender = request_obj.citizen.gender
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
        # send_status_email(request_obj.citizen.user.email, request_obj)
        send_kyc_status_email_task.delay(request_obj.citizen.user.email, id)
        return redirect("officer_home_page")
    except Exception as e:
        return redirect("officer_home_page")



def approved_requests(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
    approved_requests = KYCRequest.objects.filter(
        status="approved", reviewed_by=officer.user
    ).order_by("-reviewed_at")
    return render(
        request,
        "list_requests.html",
        {"requests": approved_requests, "status": "approved"},
    )



def rejected_requests(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
    rejected_requests = KYCRequest.objects.filter(
        status="rejected", reviewed_by=officer.user
    ).order_by("-reviewed_at")
    return render(
        request,
        "list_requests.html",
        {"requests": rejected_requests, "status": "rejected"},
    )



def search_request(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        logout(request)
        return redirect("kyc_app")
    search_input = request.POST.get("searchinput")

    requests = KYCRequest.objects.filter(
        (
            Q(request_id=search_input)
            | Q(citizen__phone_number=search_input)
            | Q(citizen__user__email=search_input)
            | Q(citizen__full_name__iexact=search_input)
        )
        & Q(status="pending")
    )
    context = {
        "requests": requests,
        "search_result": True,
        "status": "pending",
        "search_input": search_input,
    }
    return render(request, "list_requests.html", context)



def show_log(request, id):
    request_obj = KYCRequest.objects.get(id=id)
    log = RejectedRequest.objects.filter(request_obj=request_obj)
    context = {"request_obj": request_obj, "log": log}
    try:
        officer = Officer.objects.get(user=request.user)
        return render(request, "log_list.html", context)
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        if request_obj.citizen != citizen_obj:
            return HttpResponseForbidden("You are not allowed to view this request.")
        return render(request, "log_list.html", context)

def log_details(request, id):
    request_obj = RejectedRequest.objects.get(id=id)
    context = {"request_obj": request_obj}
    try:
        officer = Officer.objects.get(user=request.user)
        return render(request, "log_details.html", context)
    except Officer.DoesNotExist:
        citizen_obj = Citizen.objects.get(user=request.user)
        if request_obj.citizen != citizen_obj:
            return HttpResponseForbidden("You are not allowed to view this request.")
        return render(request, "log_details.html", context)
