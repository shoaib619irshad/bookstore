from django.urls import path

from .views import AddView, DisplayView

urlpatterns = [
    path('add/', AddView.as_view(), name='add_book'),
    path('view/', DisplayView.as_view(), name='view_book')
]