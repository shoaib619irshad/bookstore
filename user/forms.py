from django import forms
from django.contrib.auth import password_validation as validators

from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    email = forms.EmailField(max_length=101, required=True)
    password = forms.CharField(max_length=128, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.CharField(max_length=8, required=True)
    phone = forms.CharField(max_length=10, required=True)


class UserLoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


    email = forms.EmailField(max_length=101, required=True)
    password = forms.CharField(max_length=128, required=True)