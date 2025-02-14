from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    
]