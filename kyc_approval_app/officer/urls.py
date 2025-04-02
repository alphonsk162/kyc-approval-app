from django.urls import path
from .views import (
    officer_login,
    officer_home_page,
    officer_signin,
    view_request,
    approve_request,
    approved_requests,
    reject_request,
    rejected_requests,
)

urlpatterns = [
    path("officer_login/", officer_login, name="officer_login"),
    path("officer_signin/", officer_signin, name="officer_signin"),
    path("officer_home_page/", officer_home_page, name="officer_home_page"),
    path("view_request/<int:id>/", view_request, name="view_request"),
    path("approve_request/<int:id>/", approve_request, name="approve_request"),
    path("approved_requests", approved_requests, name="approved_requests"),
    path("reject_request/<int:id>/", reject_request, name="reject_request"),
    path("rejected_requests", rejected_requests, name="rejected_requests"),
]
