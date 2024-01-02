from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=101)
    password = forms.CharField(max_length=128)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    role = forms.CharField(max_length=8)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'first_name', 'last_name', 'role', 'phone']