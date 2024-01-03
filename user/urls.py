from django.urls import path

from user.views import HomeView , RegisterView, Register

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
]