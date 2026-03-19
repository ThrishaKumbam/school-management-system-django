from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from school_system_app.custom_auth import CustomTokenAuthentication

custom_token_obj = CustomTokenAuthentication()
def get_user(request):
    return custom_token_obj.authenticate(request)

class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "The Django authentication middleware requires session "
                "middleware to be installed. Edit your MIDDLEWARE setting to "
                "insert "
                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                "'django.contrib.auth.middleware.AuthenticationMiddleware'."
            )
        request.user = get_user(request)[0]
        