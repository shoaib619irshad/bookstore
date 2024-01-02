from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.shortcuts import render

from .forms import UserRegistrationForm

class HomeView(TemplateView):
	template_name = 'home.html'
	

class RegisterView(View):
	def post(self, request, *args, **kwargs):
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, 'register.html')
	
class Register(TemplateView):
	template_name = 'register.html'