from .models import Citizen
from django.contrib import messages
from django.contrib.auth.models import User
import phonenumbers
from user.models import KYCRequest


def validate(request, password, password_copy, email_id, phone_number):
    if password != password_copy:
        messages.error(request, "Passwords did not match, Please try again.")
        return False

    parsed_number = phonenumbers.parse(phone_number, "IN")
    if not (
        phonenumbers.is_valid_number(parsed_number)
        and phonenumbers.is_possible_number(parsed_number)
    ):
        messages.error(request, "Enter a valid Indian mobile number.")
        return False

    existing_usernames = list(User.objects.values_list("username", flat=True))
    for existing_username in existing_usernames:
        if email_id == existing_username:
            messages.error(
                request,
                "This email already exists. Please try using another email ID.",
            )
            return False

    existing_phones = list(Citizen.objects.values_list("phone_number", flat=True))
    for existing_phone in existing_phones:
        if phone_number[::-1][:10][::-1] == existing_phone:
            messages.error(
                request,
                "This Phone number already exists. Please try using another Phone number.",
            )
            return False
    messages.success(request, "Your account registered successfully.")
    return True


def find_submitted_requests(user):
    citizen_obj = Citizen.objects.get(user=user)
    requests = KYCRequest.objects.filter(citizen=citizen_obj)
    return requests
