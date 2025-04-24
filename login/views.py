from django.shortcuts import render,redirect
from .forms import CustomCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def user_signup(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST,request.FILES)   
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'Account created Successfully  You are now logged in')
            return redirect('home:index')
        else:
            messages.error(request,'There was an issue with your sign-up. Please try again.')
            print(form.errors)
    else:
        form = CustomCreationForm()
    return render(request, 'registration/signup.html',{'form':form})


def login_user(request):
    if request.method == 'POST':
        user_or_email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username = user_or_email, password = password)
        if user is None:
            try:
                user_obj = User.objects.get(email = user_or_email)
                user = authenticate(request, username = user_obj.username, password = password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request,user)
            messages.success(request, f'👋 Welcome back, {user.username}!')
            return redirect('home:index')
        else:
            messages.error(request, "❌ Invalid credentials. Please try again.")
    return render(request, 'registration/login.html',{'form':CustomCreationForm()})


