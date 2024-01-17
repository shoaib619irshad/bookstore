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
        uid = request.GET.get('u_id')
        user = CustomUser.objects.filter(id=uid).first()
        bname = request.GET.get('b_name')
        book = Books.objects.filter(name=bname).first()
        
        return render(request, 'order_book.html', {'user':user, 'book':book})
    
    def post(self, request, *args, **kwargs):
        uid = request.GET.get('u_id')
        user = CustomUser.objects.filter(id=uid).first()
        bname = request.GET.get('b_name')
        book = Books.objects.filter(name=bname).first()
        
        book.status=Books.ORDERED
        book.ordered_by = user
        book.save()
        bc = BookCart.objects.filter(name=bname)
        if bc:
            bc.delete()
        messages.success(request, 'Order placed successfully')
        return redirect('order_book')
    

class ReturnView(View):
    def get(self, request, *args, **kwargs):
        id = (request.GET.get('u_id'))
        user = CustomUser.objects.filter(id=id).first()
        books = Books.objects.filter(ordered_by=user)
        return render(request, 'return_book.html', {'books':books, 'user':user})
    
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

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')
    
    def post(self, request, *args, **kwargs):
        old_password = request.POST['old_pass']
        new_password = request.POST['new_pass']
        confirm_password = request.POST['c_pass']
        user_id = request.GET.get('user')
        user = CustomUser.objects.filter(id=user_id).first()
        if not user.check_password(old_password):
            messages.error(request, 'Old password does not match.You can try forgot password')
            return render(request , 'result.html')
        if old_password == new_password:
            messages.error(request, 'New Password cannot be old password')
            return render(request, 'change_password.html')
        if new_password != confirm_password:
            messages.error(request, 'Password does not match')
            return render(request, 'change_password.html')
        
        user.password = make_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully.Please Login again.')
        return render(request, 'result.html')
       

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
    

class UpdateProfileView(View):
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('u_id')
        user = CustomUser.objects.filter(id=uid).first()
        return render(request, 'update_profile.html', {'user':user})