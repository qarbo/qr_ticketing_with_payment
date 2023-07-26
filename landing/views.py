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


def booking_page(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    return render(request, 'booking.html', {'username': username})


def landing_page(request):
    return render(request, 'landing.html', )


def logout_view(request):
    logout(request)
    return redirect('landing_page')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('booking_page')  # Replace 'home' with the URL name of your home view or URL pattern.
        else:
            # Invalid credentials. You can display an error message on the login page.
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


endpoint_secret = 'test'


@csrf_exempt
def stripe_webhook(request, ):
    payload = request.body
    event = None
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle specific webhook events here
    # Example:
    if event.type == 'payment_intent.succeeded':
        # Handle successful payment
        payment_intent = event.data.object
        # Process the payment or perform any other required actions

    return JsonResponse({'status': 'success'})
