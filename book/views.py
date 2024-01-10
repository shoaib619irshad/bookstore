from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Books
from user.models import CustomUser

class AddView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'add_book.html')
    
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        author = request.POST['author']
        p_year = request.POST['p_year']
        book = Books(name=name, author=author, published_year=p_year)
        c_book = Books.objects.filter(name=name, author=author, published_year=p_year)
        if c_book:
            messages.error(request, 'This book already exists')
            return redirect('add_book')
        
        book.save()
        messages.success(request, 'Book added successfully')
        return redirect('add_book')
    
class DisplayView(View):
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        return render(request, 'view_books.html', {'books':books})
    
    
class DeleteView(View):
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        return render(request, 'delete_book.html', {'books':books})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['book']
        book = Books.objects.filter(name=name).first()
        book.delete()
        messages.success(request, 'Book deleted successfully')
        return redirect('delete_book')
    

class OrderView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('user')
        books = Books.objects.all()
        return render(request, 'order_book.html', {'books':books, 'user':email})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['book']
        book =  Books.objects.filter(name=name).first()
        email = request.GET.get('user')
        user = CustomUser.objects.filter(email=email).first()
        book.status=Books.ORDERED
        book.ordered_by = user
        book.save()
        messages.success(request, 'Order placed successfully')
        return redirect('order_book')
    

class ReturnView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('user')
        books = Books.objects.all()
        return render(request, 'return_book.html', {'books':books, 'user':email})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['book']
        book =  Books.objects.filter(name=name).first()
        book.status=Books.AVAILABLE
        book.ordered_by = None
        book.save()
        messages.success(request, 'Book returned successfully')
        return redirect('return_book')
    

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')