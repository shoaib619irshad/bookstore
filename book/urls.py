from django.urls import path

from .views import *

urlpatterns = [
    path('add/', AddView.as_view(), name='add_book'),
    path('view/', DisplayView.as_view(), name='view_book'),
    path('issue/', IssueView.as_view(), name='issue_book'),
    path('books/', IssuedBookView.as_view(), name='issued_books'),
    path('delete/', DeleteView.as_view(), name='delete_book')
]