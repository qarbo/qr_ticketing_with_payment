from datetime import timedelta
from typing import Optional

import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from booking.forms import BookingForm
from booking.models import Booking, Table
from little_elista import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='login')
def booking_page(request):
    if request.user.bookings.all():
        return redirect("last_booking")
    email = request.user.email
    form = BookingForm()
    return render(request, 'booking.html', {'form': form, 'email': email})


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        table: Optional[Table] = None
        if request.user.bookings.all():
            booking = request.user.bookings.order_by('-created_at').first()
        else:
            booking = Booking()
            booking.user = request.user
        if table_ids := request.POST['tables']:
            table = get_object_or_404(Table, pk=table_ids[0])
            for current_table in booking.tables.all():
                current_table.booking = None
                current_table.save()
            table.booking = booking
            table.save()
        booking.bar_guests = request.POST['bar_guests']
        booking.save()
        line_items = []
        if int(booking.bar_guests) > 0:
            line_items.append(
                {
                    "price": settings.STRIPE_SINGLE_PASS_PRICE,
                    "quantity": booking.bar_guests
                }
            )
        if table:
            line_items.append(
                {
                    "price": table.stripe_price,
                    "quantity": 1
                }
            )

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=f"{request.META['HTTP_ORIGIN']}/booking/success/?booking={booking.payment_uuid}",
            cancel_url=f"{request.META['HTTP_ORIGIN']}/",
        )
        return redirect(checkout_session.url)


@login_required(login_url='login')
def last_booking(request):
    if request.user.bookings.all():
        booking = request.user.bookings.order_by('-created_at').first()
        form = BookingForm(instance=booking, user_id=request.user.id)
        pay_by = booking.created_at + timedelta(minutes=15)
        return render(
            request, 'last_booking.html', {'form': form, 'pay_by': pay_by, 'booking': booking}
        )
    else:
        redirect('booking_page')


def delete_booking(request, pk):
    obj = get_object_or_404(Booking, id=pk)
    obj.delete()
    return redirect('booking_page')


def success(request):
    print(request)
    return redirect('landing_page')


def booking_info(request):
    print(request)
    return redirect('landing_page')

