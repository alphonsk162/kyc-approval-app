from django.db import models
from django.contrib.auth.models import User
from user.models import KYCRequest


# Create your models here.


class RejectedRequest(models.Model):
    request_obj = models.ForeignKey(KYCRequest, on_delete=models.CASCADE, null=True)
    request_full_name = models.CharField(max_length=255)
    request_dob = models.DateField()
    request_address = models.TextField()
    request_gender = models.CharField(max_length=10)
    request_phone_number = models.CharField(max_length=20)
    request_email = models.EmailField()
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_proof_name = models.CharField(max_length=20)
    address_proof_name = models.CharField(max_length=20)
    submitted_at = models.DateTimeField()
    reviewed_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    id_proof_file = models.FileField(upload_to="id_proofs/")
    address_proof_file = models.FileField(upload_to="address_proofs/")
