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
    def get(self, request, book_id, *args, **kwargs):
        if request.path == f"/book/order/{book_id}/":
            book = Books.objects.filter(id=book_id).first()
            return render(request, 'order_book.html', {'book':book})
        
        elif request.path == f"/cart/order/{book_id}/":
            book1 = BookCart.objects.filter(id=book_id).first()
            book = Books.objects.filter(name=book1.name).first()
            return render(request, 'order_book.html', {'book':book})

    
    def post(self, request, book_id, *args, **kwargs):
        user = request.user
        if request.path == f"/book/order/{book_id}/":
            book = Books.objects.filter(id=book_id).first()

        elif request.path == f"/cart/order/{book_id}/":
            book1 = BookCart.objects.filter(id=book_id).first()
            book = Books.objects.filter(name=book1.name).first()
        
        book.status=Books.ORDERED
        book.ordered_by = user
        book.save()
        bc = BookCart.objects.filter(name=book.name)
        if bc:
            bc.delete()
        messages.success(request, 'Order placed successfully')
        return render(request, 'order_book.html')
    

class ReturnView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        books = Books.objects.filter(ordered_by=user)
        return render(request, 'return_book.html', {'books':books})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['book']
        book =  Books.objects.filter(name=name).first()
        book.status=Books.AVAILABLE
        book.ordered_by = None
        book.save()
        messages.success(request, 'Book returned successfully')
        return redirect('return_book')
    

class AddToCartView(View):
    def get(self, request, book_id, *args, **kwargs):
        user = request.user
        book = Books.objects.filter(id=book_id).first()
        bc = BookCart(name=book.name, added_by=user, status=BookCart.ADDED)
        c_bc = BookCart.objects.filter(name=book.name, added_by=user)
        if c_bc:
            return redirect('view_cart')
        
        bc.save()
        return redirect('view_cart')
    

class CartView(View):
    def get(self, request, *args, **kwargs):
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'bookscart':bookscart,})


class RemoveView(View):
    def get(self, request, book_id, *args, **kwargs):
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'bookscart':bookscart, 'confirm':'confirm'})
    
    def post(self, request, book_id, *args, **kwargs):
        book = BookCart.objects.filter(id=book_id).first()
        if not book:
            bookscart = BookCart.objects.all()
            return render(request, 'cart.html', {'bookscart':bookscart})

        book.delete()
        bookscart = BookCart.objects.all()
        return render(request, 'cart.html', {'bookscart':bookscart})