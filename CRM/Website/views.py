from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *

# Create your views here.
def home(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'There you GOOO!! . You are now logged in')
            return render(request, 'home.html')
        else:    
            messages.error(request, '!!Holy Cow!! Wrong credentials.')
            return render(request, 'home.html')

    return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Bye Bye, You are logged out')
    return render(request,'home.html')  



def register_user(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'You are Registered')
            return render(request,'home.html')
        else:
            form = SignUpForm()
            return render(request, 'register.html', {'form':form})
      
    return render(request, 'register.html')
        
def add_record(request):
	form = Addrecords(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'addrecord.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	