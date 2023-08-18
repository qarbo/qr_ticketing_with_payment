import uuid

from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.utils.translation import gettext as _


class Booking(models.Model):

    CHOICES = (
        ('regular_pass', 'Regular pass / Стандартный вход'),
        ('table', 'Table / Бронь стола'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'))
    fullname = models.CharField(max_length=512)
    bar_guests = models.PositiveIntegerField(default=0)
    checked_guests = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    selected_option = models.CharField(max_length=20, default='regular_pass', choices=CHOICES)

    # Add more fields as per your application's requirements

    def __str__(self):
        return f"{self.fullname} ({self.email}) - {self.id} ({self.created_at})"


class Zone(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Table(models.Model):
    number_of_seats = models.IntegerField()
    full_price = models.FloatField()
    deposit = models.FloatField()
    name = models.CharField(max_length=32)
    zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL, related_name='tables')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='tables')
    stripe_price = models.CharField(max_length=256)


    def __str__(self):
        if self.zone:
            return f"{self.zone.name} {self.name} - {self.number_of_seats} seats"
        else:
            return f"{self.name} - {self.number_of_seats} seats"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Add more fields as per your application's requirements

    def __str__(self):
        return f"Booking: {self.booking} - Amount: {self.amount}"


class CheckIn(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkins')
    guests_checked_in = models.PositiveIntegerField(default=0)
    checkin_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.booking} - When: {self.checkin_time}"
