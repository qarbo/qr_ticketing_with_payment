from django.contrib import admin

from booking.models import Booking, Payment, Table, Zone

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Zone)
admin.site.register(Table)
