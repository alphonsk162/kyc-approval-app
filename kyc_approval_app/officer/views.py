from django.shortcuts import render, redirect
from .models import RejectedRequest
from Accounts.models import Officer
from django.contrib.auth.decorators import login_required
from user.models import KYCRequest
from django.utils import timezone
from .helper_functions import send_status_email
from django.db.models import Q

# Create your views here.


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
    # try:
    #     officer = Officer.objects.get(user=request.user)
    #     context["officer"] = True
    # except Officer.DoesNotExist:
    #     pass
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


@login_required(login_url="officer_login")
def search_request(request):
    try:
        officer = Officer.objects.get(user=request.user)
    except Officer.DoesNotExist:
        return redirect("user_home_page")
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


@login_required(login_url="user_login")
def show_log(request, id):
    # try:
    #     officer = Officer.objects.get(user=request.user)
    # except Officer.DoesNotExist:
    #     return redirect("user_home_page")
    request_obj = KYCRequest.objects.get(id=id)
    log = RejectedRequest.objects.filter(request_obj=request_obj)
    context = {"request_obj": request_obj, "log": log}
    return render(request, "log_list.html", context)


@login_required(login_url="user_login")
def log_details(request, id):
    # try:
    #     officer = Officer.objects.get(user=request.user)
    # except Officer.DoesNotExist:
    #     return redirect("user_home_page")
    request_obj = RejectedRequest.objects.get(id=id)
    context = {"request_obj": request_obj}
    return render(request, "log_details.html", context)
