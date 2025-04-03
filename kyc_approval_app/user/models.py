from django.db import models
from Accounts.models import Citizen
from django.contrib.auth.models import User

# Create your models here.


class KYCRequest(models.Model):
    ID_PROOF_CHOICES = [
        ("Aadhaar", "Aadhaar"),
        ("PAN", "PAN Card"),
        ("DL", "Driving License"),
        ("Passport", "Passport"),
        ("Voter ID", "Voter ID"),
    ]

    ADDRESS_PROOF_CHOICES = [
        ("Aadhaar", "Aadhaar"),
        ("Passport", "Passport"),
        ("Voter ID", "Voter ID"),
        ("Electricity Bill", "Electricity Bill"),
        ("Water Bill", "Water Bill"),
        ("Bank Statement", "Bank Statement"),
        ("Rent Agreement", "Rent Agreement"),
    ]
    id_proof_name = models.CharField(max_length=20, choices=ID_PROOF_CHOICES)
    address_proof_name = models.CharField(max_length=20, choices=ADDRESS_PROOF_CHOICES)
    citizen = models.ForeignKey(
        Citizen, on_delete=models.CASCADE, related_name="kyc_requests"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    id_proof_file = models.FileField(upload_to="id_proofs/", null=True, blank=True)
    address_proof_file = models.FileField(
        upload_to="address_proofs/", null=True, blank=True
    )
    request_full_name = models.CharField(max_length=255, null=True)
    request_dob = models.DateField(null=True, blank=True)
    request_address = models.TextField(null=True)
    request_gender = models.CharField(max_length=10, null=True)
    request_phone_number = models.CharField(max_length=20, null=True, blank=True)
    request_email = models.EmailField(null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    request_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"KYC Request for {self.citizen.full_name} - {self.status}"
