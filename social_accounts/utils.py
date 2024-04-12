from google.auth.transport import requests
from google.oauth2 import id_token
from main.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class Google():
    
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request())
            if "accounts.google.com" in id_info['iss']:
                return id_info
        except Exception as e:
            return "token is invalid or has expired"
        
def login_social_user(email, password):
    user=authenticate(email=email, password=password)
    user_tokens = user.tokens()

    return {
        'email': user.email,
        'full_name': user.get_full_name,
        'refresh_token': str(user_tokens.get('refresh_token')), 
        'access_token': str(user_tokens.get('access_token')), 
    }
        
def register_social_user(provider, email, first_name, last_name):
        user=User.objects.filter(email=email)
        
        if user.exists():
            if provider == user[0].auth_provider:
                return login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
            else:
                raise AuthenticationFailed(
                    detail=f"please continue your login with {user[0].auth_provider}"
                )
        new_user={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'auth_provider': provider,
            'password': settings.SOCIAL_AUTHS_PASSWORD,
            'is_verified': False
        }
        register_user=User.objects.create_user(**new_user)
        return login_social_user(register_user.email, settings.SOCIAL_AUTH_PASSWORD)
        