from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User

#from .models import User
from .forms import CreateUserForm

#from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('consultations:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('consultations:index')
            else:
                messages.error(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='accounts:login')
def logoutPage(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def profilePage(request):
    user= User.objects.get(pk=request.user.id)
    context = {
        'username' : user.username
        
    }
    return render(request,'accounts/profile.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('consultations:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            print("POST")
            form = CreateUserForm(request.POST)
            print(form)
            if form.is_valid():
                user = form.cleaned_data.get('username')
                form.save()
                messages.success(request, 'Account was created for ' + user)
                requestersGroup = Group.objects.get(name='requesters')
                user = User.objects.filter(username=user)
                requestersGroup.user_set.add(user[0].id)
                return redirect('accounts:login')
            else:
                messages.error(request, form.errors)
            

        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def changePage(request):
    pass
    

