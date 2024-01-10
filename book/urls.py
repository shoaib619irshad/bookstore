from django.urls import path

from .views import *

urlpatterns = [
    path('add/', AddView.as_view(), name='add_book'),
    path('view/', DisplayView.as_view(), name='view_book'),
    path('delete/', DeleteView.as_view(), name='delete_book'),
    path('order/', OrderView.as_view(), name='order_book'),
    path('return/', ReturnView.as_view(), name='return_book'),
    path('change_pass/', ChangePasswordView.as_view(), name='change_password'),
]