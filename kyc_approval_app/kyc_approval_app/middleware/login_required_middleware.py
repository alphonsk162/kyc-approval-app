from django.shortcuts import redirect
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_names = [
            'login',
            'index',
            'kyc_app',
            'officer_login',
            'officer_signin',
            'user_signup',
            'user_login',
            'register_user',
            'user_signin',
        ]
        self.redirect_url = 'kyc_app' 

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name


        if url_name in self.exempt_names:
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return redirect(self.redirect_url)

        return self.get_response(request)

