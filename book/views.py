from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from .models import Books, BookCart
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
        bid = request.GET.get('bid')
        book = Books.objects.filter(id=bid).first()
        return render(request, 'order_book.html', {'book':book})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        bid = request.GET.get('bid')
        book = Books.objects.filter(id=bid).first()
        
        book.status=Books.ORDERED
        book.ordered_by = user
        book.save()
        bc = BookCart.objects.filter(name=book.name)
        if bc:
            bc.delete()
        messages.success(request, 'Order placed successfully')
        return redirect('order_book')
    

class ReturnView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        books = Books.objects.filter(ordered_by=user)
        return render(request, 'return_book.html', {'books':books, 'check':'check'})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['book']
        book =  Books.objects.filter(name=name).first()
        book.status=Books.AVAILABLE
        book.ordered_by = None
        book.save()
        messages.success(request, 'Book returned successfully')
        return redirect('return_book')
    

class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('u_id')
        bname= request.GET.get('b_name')
        user = CustomUser.objects.filter(id=uid).first()
        book = Books.objects.filter(name=bname).first()
        bc = BookCart(name=book.name, author=book.author, published_year=book.published_year, added_by=user)
        c_bc = BookCart.objects.filter(name=book.name, author=book.author, published_year=book.published_year, added_by=user)
        bookscart = BookCart.objects.all()
        if c_bc:
            return render(request, 'cart.html', {'bookscart':bookscart, 'user':user})
        
        bc.save()
        return render(request, 'cart.html', {'bookscart':bookscart, 'user':user})
    

class CartView(View):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'bookscart':bookscart, 'user':user})


class RemoveView(View):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('u_id')
        user = CustomUser.objects.filter(id=uid).first()
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'bookscart':bookscart, 'user':user, 'confirm':'confirm'})
    
    def post(self, request,*args, **kwargs):
        uid = request.GET.get('u_id')
        user = CustomUser.objects.filter(id=uid).first()
        bid = request.GET.get('b_id')
        book = BookCart.objects.filter(id=bid).first()
        if not book:
            bookscart = BookCart.objects.all()
            return render(request, 'cart.html', {'user':user, 'bookscart':bookscart})

        book.delete()
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'user':user, 'bookscart':bookscart})