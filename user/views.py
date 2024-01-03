from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser

class HomeView(TemplateView):
	template_name = 'home.html'
	

class RegisterView(View):

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            phone = form.cleaned_data['phone']
            user = CustomUser(email=email, password=password, first_name=first_name, last_name=last_name, role=role, phone=phone)
            user.save()
            messages.success(request, 'You can Login now')
            return redirect('home')
        messages.error(request, 'Email and Phone must be unique')
        return render(request, 'register.html', {'form': form})
    

class LoginView(View):
    
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if form.is_valid():
            if not user:
                messages.error(request, 'Email or password is incorrect')
                return redirect('login')
            user.last_login = timezone.now()
            user.save()
                  
        return render(request, 'about.html', {'form': form})    