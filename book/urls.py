from django.urls import path

from .views import *

urlpatterns = [
    path('book/add/', AddView.as_view(), name='add_book'),
    path('book/view/', DisplayView.as_view(), name='view_books'),
    path('book/delete/', DeleteView.as_view(), name='delete_books'),
    path('book/order/', OrderView.as_view(), name='order_book'),
    path('book/return/', ReturnView.as_view(), name='return_book'),
    path('cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('viewcart/', CartView.as_view(), name='view_cart'),
    path('remove/', RemoveView.as_view(), name='remove_from_cart'),
]