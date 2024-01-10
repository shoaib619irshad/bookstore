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
    
class IssueView(View):
    def get(self, request, *args, **kwargs):
        customers = CustomUser.objects.filter(role='customer')
        return render(request, 'issue_book.html', {'customers':customers})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        issue_to = request.POST['issued_to']
        book = Books.objects.filter(name=name).first()
        if not book:
            messages.error(request, 'Book does not found')
            return redirect('issue_book')
        
        first_name = issue_to.split(" ")[0]
        last_name = issue_to.split(" ")[1]
        user = CustomUser.objects.filter(first_name=first_name, last_name=last_name).first()
        book.issued_to = user
        book.save()
        messages.success(request, 'Book issued successfully')
        return redirect('issue_book')
    

class IssuedBookView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'issued_books.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        if not user or user.role != 'customer':
            messages.error(request, 'Email is incorrect')
            return redirect('issued_books')
        
        data = Books.objects.filter(issued_to=user.id)
        return render(request, 'view_books.html', {'user':user, 'data':data})
    
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