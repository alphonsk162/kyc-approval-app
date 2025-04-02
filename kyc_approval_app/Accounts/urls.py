from django.urls import path
from .views import (
    user_signup,
    register_user,
    user_login,
    user_home_page,
    user_signin,
    user_signout,
)

urlpatterns = [
    path("user_signup/", user_signup, name="user_signup"),
    path("register_user/", register_user, name="register_user"),
    path("user_login/", user_login, name="user_login"),
    path("user_home_page/", user_home_page, name="user_home_page"),
    path("user_signin/", user_signin, name="user_signin"),
    path("user_signout/", user_signout, name="user_signout"),
]
