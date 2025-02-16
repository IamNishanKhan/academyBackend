from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    path("password-reset/request-otp/", RequestPasswordResetOTPView.as_view(), name="request-password-reset-otp"),
    path("password-reset/verify-otp/", VerifyPasswordResetOTPView.as_view(), name="verify-password-reset-otp"),
     path("password-reset/set-password/", SetNewPasswordView.as_view(), name="set-password"),
]