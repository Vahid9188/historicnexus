from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)  # avtomatik daxil olsun
            messages.success(request, "Registration completed successfully!")
            return redirect('index')
    
    return render(request, "register.html", {"form": form})


def loginUser(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html", {"form": form})


def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")
