from django.contrib import admin
from .models import KYCRequest, RejectedRequest

# Register your models here.
class KYCRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'submitted_at', 'reviewed_at') 

admin.site.register(RejectedRequest)
admin.site.register(KYCRequest)