from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.error(request,'Email Already Exists')
                return redirect('account:register')
            elif User.objects.filter(username = username).exists():
                messages.error(request,'Username Already Exists')
                return redirect('account:register')
            else:
                #creating new user
                user = User.objects.create_user(username = username, password = password, email = email)
                user.save()
                
                #logging in new user created
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                
                return redirect('api:index')
        else:
            messages.error(request,'Password not matching...')
            return redirect('account:register')
    else:
        if request.user.is_authenticated:
            return redirect('api:index')
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('api:index')
        else:
            messages.error(request,'You are not registered. Please register.')
            return redirect('account:register')
    else:
        if request.user.is_authenticated:
            return redirect('api:index')
        return render(request,'login.html')

def logout(request):
    auth.logout(request=request)
    return redirect('account:login')
