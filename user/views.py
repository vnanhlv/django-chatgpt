from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import template
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in

# Create your views here.
def user(request):
    if not user_logged_in:
        context = {'user': 'guest'}
    context = {}
    return render(request, 'user/user.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    print(context)
    return render(request, 'user/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            print(f"Sai tài khoản hoặc mật khẩu -- admin: {username} - {password}")
            messages.info(request, 'Sai tài khoản hoặc mật khẩu')
            
    context = {}
    form = LoginForm()
    context = {'form': form}
    print(context)
    return render(request, 'user/login.html', context)

def UserLoggedIn(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'guest'
    return username

def logout_page(request):
    username = UserLoggedIn(request)
    if username != 'guest':
        logout(request)
        return redirect('home')
    else:
        return redirect('user_home')
