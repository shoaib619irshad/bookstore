from django.conf import settings
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .models import CustomUser
from book.models import Books

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
        
        login(request, user)
        user.last_login = timezone.now()
        user.save()
        return redirect('dashboard')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        return render(request, 'dashboard.html', {'books':books})
    

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')
    
    def post(self, request, *args, **kwargs):
        old_password = request.POST['old_pass']
        new_password = request.POST['new_pass']
        confirm_password = request.POST['c_pass']
        user = request.user

        if not user.check_password(old_password):
            messages.error(request, 'Old password does not match.You can try forgot password')
            return render(request , 'result.html')
        if old_password == new_password:
            messages.error(request, 'New Password cannot be old password')
            return render(request, 'change_password.html')
        if new_password != confirm_password:
            messages.error(request, 'Password does not match')
            return render(request, 'change_password.html')
        
        user.password = make_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully.Please Login again.')
        return render(request, 'result.html')
    

class UpdateProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'update_profile.html')
    
    def post(self, request, *args, **kwargs):
        user = request.user
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']

        if not email and not first_name and not last_name and not phone:
            messages.error(request, 'Provide data to update profile')
            return redirect('update_profile')
        
        if email:
            c_user = CustomUser.objects.filter(email=email).first()
            if user == c_user:
                messages.error(request, 'New email is same as old email')
                return redirect('update_profile')
            elif c_user:
                messages.error(request, 'User with this email already exists')
                return redirect('update_profile')
            user.email = email

        if first_name:
            user.first_name = first_name
            
        if last_name:
            user.last_name = last_name

        if phone:
            c_user = CustomUser.objects.filter(phone=phone).first()
            if len(phone) != 10:
                messages.error(request, 'Phone number must be 10 digits long')
                return redirect('update_profile')
            elif user == c_user:
                messages.error(request, 'New phone no is same as old phone no')
                return redirect('update_profile')
            elif c_user:
                messages.error(request, 'User with this phone no already exists')
                return redirect('update_profile')
            user.phone = phone

        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return render(request, 'result.html')
    

class ResetPasswordView(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'reset_password.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'Email does not exists')
            return redirect('reset_password')
        
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reset_url = reverse('set_password', kwargs={'uidb64': uidb64, 'token': token})
        reset_link = f'{request.scheme}://{request.get_host()}{reset_url}'
        subject = "Reset Password"
        message = f'Hi {user.first_name}, click on the link to reset your password:{reset_link}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email ,]
        send_mail( subject, message, from_email, recipient_list )
        messages.success(request, 'Password reset link has been successfully sent to your email.')
        return redirect('login')
    

class SetPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'set_password.html')
    
    def post(self, request, *args, **kwargs):
        new_password = request.POST['new_pass']
        confirm_password = request.POST['c_pass']
        uidb64 = kwargs['uidb64']
        user_id = force_str(urlsafe_base64_decode(uidb64))
        print(user_id)
        user = CustomUser.objects.filter(id=user_id).first()

        if new_password != confirm_password:
            messages.error(request, 'Password does not match')
            return render(request, 'set_password.html')
        
        user.password = make_password(new_password)
        print(new_password,"============")
        print(user.password)
        user.save()
        messages.success(request, 'Password set successfully. You can login now')
        return redirect('login')