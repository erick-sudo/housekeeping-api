from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework import exceptions

class SparkleSyncAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the access token from the HTTP-only cookie
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if not access_token:
            return None

        try:
            # Validate the token
            validated_token = self.get_validated_token(access_token)
        except exceptions.AuthenticationFailed:
            raise

        # Get the user associated with the token
        user = self.get_user(validated_token)

        return user, validated_token