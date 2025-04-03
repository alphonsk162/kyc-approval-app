from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_status_email(to_email, kyc_request):
    subject = "KYC Request Status Update"
    message_html = render_to_string(
        "kyc_status_email.html", {"kyc_request": kyc_request}
    )
    message_plain = strip_tags(message_html)
    send_mail(
        subject,
        message_plain,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
        html_message=message_html,
    )
