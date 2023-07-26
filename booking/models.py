from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()

    # Add more fields as per your application's requirements

    def __str__(self):
        return f"{self.user} - {self.check_in_date} to {self.check_out_date}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Add more fields as per your application's requirements

    def __str__(self):
        return f"Booking: {self.booking} - Amount: {self.amount}"
