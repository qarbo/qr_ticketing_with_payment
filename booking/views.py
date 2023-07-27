import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from booking.forms import BookingForm
from booking.models import Booking
from little_elista import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def booking_page(request):
    email = request.user.email
    form = BookingForm()
    return render(request, 'booking.html', {'form': form, 'email': email})


@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            booking = Booking()
            booking.user = request.user
            booking.save()
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1NXyYgEfhjLWHR5AL0793bnL",
                        "quantity": 1
                    }
                ],

                mode="payment",
                success_url=f"http://127.0.0.1:8000/booking/success/?booking={booking.uuid}",
                cancel_url="http://127.0.0.1:8000/",
            )
            return redirect(checkout_session.url)
        except Exception as e:
            pass


def success(request):
    print(request)
    return redirect('landing_page')


def booking_info(request):
    print(request)
    return redirect('landing_page')

