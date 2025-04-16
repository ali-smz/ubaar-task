from django.urls import path
from .views import (
    RequestLoginView,
    PasswordLoginView,
    OTPRequestView,
    OTPVerifyView,
    ProfileUpdateView,
    SetPasswordView
)

urlpatterns = [
    path('auth/request-login/', RequestLoginView.as_view(), name='request-login'),
    path('auth/login-password/', PasswordLoginView.as_view(), name='login-password'),
    path('auth/request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('auth/verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('auth/set-profile/', ProfileUpdateView.as_view(), name='set-profile'),
    path('auth/set-password/', SetPasswordView.as_view(), name='set-password'),
]