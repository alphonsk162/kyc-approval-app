from django.urls import path
from .views import (
    user_signup,
    register_user,
    user_login,
    user_home_page,
    user_signin,
    user_signout,
    request_kyc_approval,
    submit_request,
    edit_profile,
    update_profile,
    edit_submission,
    update_kyc_request,
)

urlpatterns = [
    path("user_signup/", user_signup, name="user_signup"),
    path("register_user/", register_user, name="register_user"),
    path("user_login/", user_login, name="user_login"),
    path("user_home_page/", user_home_page, name="user_home_page"),
    path("user_signin/", user_signin, name="user_signin"),
    path("user_signout/", user_signout, name="user_signout"),
    path("request_kyc_approval/", request_kyc_approval, name="request_kyc_approval"),
    path("submit_request/", submit_request, name="submit_request"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("update_profile/", update_profile, name="update_profile"),
    path("edit_submission/<int:id>/", edit_submission, name="edit_submission"),
    path("update_kyc_request/<int:id>/", update_kyc_request, name="update_kyc_request"),
]
