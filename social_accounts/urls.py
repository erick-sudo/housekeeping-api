from django.urls import path
from .views import GoogleSignInView

urlpatterns = [
    path('google-login', GoogleSignInView.as_view(), name='google'),
]