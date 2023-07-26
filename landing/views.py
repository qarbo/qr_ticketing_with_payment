import json

import stripe

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm


def landing_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_page')  # Redirect to a success page after registration
    else:
        if request.user.is_authenticated:
            return redirect('booking_page')
        form = RegistrationForm()

    return render(request, 'landing_page.html', {'form': form})


def booking_page(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    return render(request, 'booking.html', {'username': username})


@csrf_exempt
def stripe_webhook(request, ):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': str(e)}, status=400)

    # Handle specific webhook events here
    # Example:
    if event.type == 'payment_intent.succeeded':
        # Handle successful payment
        payment_intent = event.data.object
        # Process the payment or perform any other required actions

    return JsonResponse({'status': 'success'})
