from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.full_name
    

