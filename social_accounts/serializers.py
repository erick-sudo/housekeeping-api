from rest_framework import serializers
from .utils import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(max_length=255)
    
    def validate_access_token(self, access_token):
        google_user_data=Google.validate(access_token)
        
        try:
            user_id=google_user_data["sub"]
        except:
            raise serializers.ValidationError("this token is invalid or has expired")
        
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("could not verify user identity")
        
        email = google_user_data['email']
        first_name = google_user_data['given_name']
        last_name = google_user_data['family_name']
        provider = 'google'
        
        return register_social_user(provider=provider, email=email, first_name=first_name, last_name=last_name)