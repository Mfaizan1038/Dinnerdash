from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Welcome, Your account has been created')
            return redirect('home')
    else :
        form = RegisterForm()
    return render(request, 'accounts/register.html',{'form' :form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            next_url = request.GET.get('next','home')
            return redirect(next_url)
        else:
            messages.error(request, "wrong email or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html',{'form' :form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logout succesfull")
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form =ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile updated succesfully')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {"form", form})







