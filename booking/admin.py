from django.contrib import admin

from booking.models import Booking, Payment, Table

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Table)
