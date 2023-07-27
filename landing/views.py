import json

import stripe
from django.contrib.auth import logout, authenticate, login

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_page')  # Redirect to a success page after registration
    else:
        if request.user.is_authenticated:
            return redirect('booking_page')
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def landing_page(request):

    print(request)
    return render(request, 'landing.html', )


def logout_view(request):
    logout(request)
    return redirect('landing_page')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('booking_page')  # Replace 'home' with the URL name of your home view or URL pattern.
        else:
            # Invalid credentials. You can display an error message on the login page.
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
