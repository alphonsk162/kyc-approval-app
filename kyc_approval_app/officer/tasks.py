from celery import shared_task
from .helper_functions import send_status_email
from kyc_approval_app.models import KYCRequest

@shared_task
def send_kyc_status_email_task(to_email, id):
    kyc_request = KYCRequest.objects.get(id=id)
    send_status_email(to_email, kyc_request)
    return f"Email sent to {to_email} for KYC request {kyc_request}"
