from django.urls import path

from user.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('change_pass/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', UpdateProfileView.as_view(), name='update_profile'),
]