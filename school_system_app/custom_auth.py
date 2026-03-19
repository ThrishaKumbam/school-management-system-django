# custom_auth.py
import jwt
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from django.conf import settings
 
class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.get_token_from_request(request)
        user = self.get_user(token)
        return (user, None)

    def get_token_from_request(self,request):
        token = request.COOKIES.get('auth_token') or request.headers.get('Authorization')
        return token or None

    def get_user(self, token):
        if token:
            try:
                decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_payload.get('user_id')
                user = User.objects.get(id=user_id)
                return user or None
            except jwt.ExpiredSignatureError:
                # Handle token expired error
                return None
            except jwt.InvalidTokenError:
                # Handle invalid token error
                return None
            except User.DoesNotExist:
                # Handle user not found error
                return None
        else:
            return None
