from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from.forms import RegistrationForm, PasswordResetForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Try logging in.')
                return render(request, 'index.html', {'form': form})

            user = User(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'index.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('login')  
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username does not exist. Please register.')
            else:
                messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')


def password_reset(request):
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if not User.objects.filter(username=username).exists():
                form.add_error('username', 'Username does not exist.')
            else:
                user = User.objects.get(username=username)

                if new_password != confirm_password:
                    form.add_error('confirm_password', 'Passwords do not match.')
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password reset successful! You can now log in with your new password.')
                    return redirect('login')

    return render(request, 'password_reset.html', {'form': form})