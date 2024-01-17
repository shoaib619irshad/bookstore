from django.urls import path

from .views import *

urlpatterns = [
    path('add/', AddView.as_view(), name='add_book'),
    path('view/', DisplayView.as_view(), name='view_book'),
    path('delete/', DeleteView.as_view(), name='delete_book'),
    path('cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('viewcart/', CartView.as_view(), name='view_cart'),
    path('remove/', RemoveView.as_view(), name='remove_from_cart'),
    path('profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('order/', OrderView.as_view(), name='order_book'),
    path('return/', ReturnView.as_view(), name='return_book'),
    path('change_pass/', ChangePasswordView.as_view(), name='change_password'),
]