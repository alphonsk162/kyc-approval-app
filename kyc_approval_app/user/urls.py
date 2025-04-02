from django.urls import path
from .views import (
    request_kyc_approval,
    submit_request,
    edit_profile,
    update_profile,
    edit_submission,
    update_kyc_request,
)

urlpatterns = [
    path("request_kyc_approval/", request_kyc_approval, name="request_kyc_approval"),
    path("submit_request/", submit_request, name="submit_request"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("update_profile/", update_profile, name="update_profile"),
    path("edit_submission/<int:id>/", edit_submission, name="edit_submission"),
    path("update_kyc_request/<int:id>/", update_kyc_request, name="update_kyc_request"),
]
