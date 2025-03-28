from django.contrib.auth.models import User
from django.db import models

class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)  
    address = models.TextField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10) 


    def __str__(self):
        return self.full_name



