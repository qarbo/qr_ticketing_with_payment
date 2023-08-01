from datetime import timedelta
from io import BytesIO
from typing import Optional

import qrcode
import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from booking.forms import BookingForm
from booking.models import Booking, Table
from booking.utils import send_email_with_image, SUCCESSFULL_BOOKING_BODY, BOOKING_REQUEST_EMAIL
from little_elista import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def booking_page(request):
    form = BookingForm()
    return render(request, 'booking.html', {'form': form})


def checkout(request):
    if request.method == 'POST':
        table: Optional[Table] = None
        booking_type = request.POST['selected_option']
        booking = Booking()
        booking.save()
        if booking_type == 'regular_pass':
            booking.bar_guests = request.POST['bar_guests']
            for current_table in booking.tables.all():
                current_table.booking = None
                current_table.save()
        else:
            if table_ids := request.POST['tables']:
                table = get_object_or_404(Table, pk=table_ids[0])
                for current_table in booking.tables.all():
                    current_table.booking = None
                    current_table.save()
                table.booking = booking
                table.save()
                booking.bar_guests = 0
        booking.email = request.POST['email']
        booking.fullname = request.POST['fullname']
        booking.selected_option = booking_type
        booking.save()
        line_items = []
        table_string = f"<li><strong>Table / Стол:</strong>{table}</li>" if table else ""
        # send_email_with_image(
        #     booking.email,
        #     "Booking Request Confirmation - Asia Days",
        #     BOOKING_REQUEST_EMAIL.format(
        #         fullname=booking.fullname,
        #         booking_link=f"{request.build_absolute_uri('/')}booking/last_booking/{booking.id}",
        #         table=table_string
        #     )
        # )
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
            success_url=f"{request.build_absolute_uri('/')}booking/success/?booking={booking.payment_uuid}",
            cancel_url=f"{request.build_absolute_uri('/')}",
        )
        return redirect(checkout_session.url)


def last_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    table = None
    if tables := booking.tables.all():
        table = tables[0]
    # booking = request.user.bookings.order_by('-created_at').first()
    form = BookingForm(instance=booking, table_id=table.id if table else None)
    pay_by = booking.created_at + timedelta(minutes=15)
    table = booking.tables.all()[0] if booking.tables.all() else None
    return render(
        request,
        'last_booking.html',
        {'form': form, 'pay_by': pay_by, 'booking': booking, 'table': table}
    )




def delete_booking(request, pk):
    obj = get_object_or_404(Booking, id=pk)
    obj.delete()
    return redirect('booking_page')


def success(request):
    booking_payment_id = request.GET["booking"]
    booking = Booking.objects.get(payment_uuid=booking_payment_id)
    booking.paid = True
    booking.save()
    email_body = SUCCESSFULL_BOOKING_BODY.format(
        fullname=booking.fullname,
        booking_id=booking.id,
        booking_link=f"{request.build_absolute_uri('/')}booking/success/?booking={booking.payment_uuid}",
        qr_code_url=f"{request.build_absolute_uri('/')}booking/generate-qr-code/{booking.id}")
    send_email_with_image(booking.email, "Booking Confirmation - Asia Days", email_body)
    return redirect('last_booking', booking_id=booking.id)


def generate_qr_code(request, booking_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(f"{request.build_absolute_uri('/')}booking/scan?booking_id={booking_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to bytes
    buffer = BytesIO()
    img.save(buffer)
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def booking_info(request):
    print(request)
    return redirect('landing_page')


@csrf_exempt
def get_price(request):
    price = 0
    booking_type = request.POST['type']
    value = request.POST.get('value', None)
    if booking_type == "regular_pass":
        price = settings.SINGLE_PASS_PRICE * (int(value) if value else 0)
    if booking_type == "table":
        if value:
            table = Table.objects.get(pk=value)
            price = table.full_price
    return JsonResponse(
        {
            "price": price
        }
    )
