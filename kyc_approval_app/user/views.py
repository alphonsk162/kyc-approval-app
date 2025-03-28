from django.shortcuts import render, redirect
from Accounts.models import Citizen
from .models import KYCRequest
# Create your views here.

def request_kyc_approval(request):
    citizen_obj = Citizen.objects.get(user=request.user)
    full_name = citizen_obj.full_name
    dob = citizen_obj.dob
    gender = citizen_obj.gender
    address = citizen_obj.address
    phone = citizen_obj.phone_number
    context = {'full_name': full_name, 'dob': dob, 'gender':gender, 'address':address, 'phone': phone, 'email': request.user.email}
    return render(request, 'kyc_request_form.html', context)

def submit_request(request):
    citizen_obj = Citizen.objects.get(user=request.user)
    id_proof_name = request.POST.get('id_proof_name')
    address_proof_name = request.POST.get('address_proof_name')
    id_proof_file = request.FILES["id_proof_file"]
    address_proof_file = request.FILES["address_proof_file"]
    KYCRequest.objects.create(citizen=citizen_obj, id_proof_name=id_proof_name, address_proof_name=address_proof_name,id_proof_file=id_proof_file,address_proof_file=address_proof_file)
    return redirect('user_home_page')

def edit_profile(request):
    citizen_obj = Citizen.objects.get(user=request.user)
    full_name = citizen_obj.full_name
    dob = citizen_obj.dob
    gender = citizen_obj.gender
    address = citizen_obj.address
    phone = citizen_obj.phone_number
    context = {'full_name': full_name, 'dob': dob, 'gender':gender, 'address':address, 'phone': phone, 'email': request.user.email}
    return render(request, 'edit_profile.html', context)

def update_profile(request):
    citizen_obj = Citizen.objects.get(user=request.user)
    full_name = request.POST.get('full_name')
    dob = request.POST.get('dob')
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')
    email_id = request.POST.get('email')
    gender = request.POST.get('gender')
    request.user.username = email_id
    request.user.email = email_id
    request.user.save()
    citizen_obj.full_name = full_name
    citizen_obj.dob = dob
    citizen_obj.address = address
    citizen_obj.phone_number = phone_number
    citizen_obj.gender = gender
    citizen_obj.save()
    return redirect('edit_profile') 

def edit_submission(request, id):
    kyc_request = KYCRequest.objects.get(id=id)
    citizen_obj = Citizen.objects.get(user=request.user)
    full_name = citizen_obj.full_name
    dob = citizen_obj.dob
    gender = citizen_obj.gender
    address = citizen_obj.address
    phone = citizen_obj.phone_number
    context = {'full_name': full_name, 'dob': dob, 'gender':gender, 'address':address, 'phone': phone, 'email': request.user.email, 'kyc_request':kyc_request}
    return render(request, 'edit_submission.html', context)

def update_kyc_request(request, id):
    kyc_request = KYCRequest.objects.get(id=id)
    id_proof_name = request.POST.get('id_proof_name')
    address_proof_name = request.POST.get('address_proof_name')
    if request.FILES.get("id_proof_file"):
        kyc_request.id_proof_file = request.FILES["id_proof_file"]
    if request.FILES.get("address_proof_file"):
        kyc_request.address_proof_file = request.FILES["address_proof_file"]
    kyc_request.id_proof_name = id_proof_name
    kyc_request.address_proof_name = address_proof_name
    kyc_request.save()
    return redirect('edit_submission', id=id)