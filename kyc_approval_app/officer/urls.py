from django.urls import path
from .views import officer_login, officer_home_page, officer_signin

urlpatterns = [
    path("officer_login/", officer_login, name="officer_login"),
    path("officer_signin/", officer_signin, name="officer_signin"),
    path("officer_home_page/", officer_home_page, name="officer_home_page"),
]