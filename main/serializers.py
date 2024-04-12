from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class UserRegisterResializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password_confirmation=serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model=User
        fields=['email', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirmation']
        
    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirmation = attrs.get('password_confirmation', '')
        if password != password_confirmation:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model=User
        fields=['email', 'password', 'full_name', 'access_token', 'refresh_token']
        
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("invalid credentials, please try again")
        
        if not user.is_verified:
            raise AuthenticationFailed("account not verified, please verify your account")
        
        user_tokens = user.tokens()
        
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'refresh_token': str(user_tokens.get('refresh_token')), 
            'access_token': str(user_tokens.get('access_token')), 
        }
        
class PasswordResetRequestViewSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    
    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            if not user.is_verified:
                raise AuthenticationFailed("account not verified, please verify your account")
            
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            sites_domain = get_current_site(request).domain
            relative_link = f"/reset_password/{uidb64}/{token}"
            # relative_link = reverse('confirm-password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absolute_link = f"{settings.FRONT_END_URL}{relative_link}"
            email_body=f"Hello {user.first_name}, use the link below to reset your password \n {absolute_link}"
            
            data = {
                'email_body': email_body,
                'email_subject': "Password reset",
                'to_email': user.email
            }
            
            send_normal_email(data)
        else:
            raise AuthenticationFailed(detail=f"User by email {email} does not exist")
        
        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password_confirmation=serializers.CharField(max_length=68, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)
    
    class Meta:
        fields=['password', 'password_confirmation', 'uidb64', 'token']
        
    def validate(self, attrs):
        token = attrs.get('token', '')
        uidb64 = attrs.get('uidb64', '')
        password = attrs.get('password', '')
        password_confirmation = attrs.get('password_confirmation', '')
        
        user = None
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except Exception as e:
            raise AuthenticationFailed("link is invalid or has expired", 401)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed("reset link is invalid or has expired", 401)
        
        if password!= password_confirmation:
            raise AuthenticationFailed("passwords do not match", 422)
        
        user.set_password(password)
        user.save()
        return user
    
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    default_error_message={
        'bad-token': ('Token is Invalid or has expired')
    }
    
    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return super().validate(attrs)
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        return super().save(**kwargs)