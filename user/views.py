from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError

from .models import CustomUser

class HomeView(TemplateView):
	template_name = 'home.html'
	

class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password != c_password:
            messages.error(request, 'Passwords does not match')
            return render(request, 'register.html')
        password = make_password(request.POST['password'])
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = request.POST['role']
        phone = request.POST['phone']
        if len(phone) != 10:
            messages.error(request, 'Phone number must be 10 digits long')
            return render(request, 'register.html')

        user = CustomUser(email=email, password=password, first_name=first_name, last_name=last_name, role=role, phone=phone)
        try:
            user.save()
            messages.success(request, 'You can Login now')
            return redirect('home')
        except IntegrityError:
            messages.error(request, 'Email and Phone must be unique')
            return render(request, 'register.html')
    

class LoginView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if not user:
            messages.error(request, 'Email or password is incorrect')
            return redirect('login')
        
        user.last_login = timezone.now()
        user.save()
        return render(request, 'dashboard.html', {'user': user})    