from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            user = UserProfile.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, username=username, address=address, password=password)
            user.save()
            messages.success(request, 'Registration is Successful!')
            return redirect('register')
    else:
        form = RegistrationForm()       
    context = {
       'form' : form,
    }
    return render(request, 'useraccounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')    

    return render(request, 'useraccounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'useraccounts/dashboard.html')    