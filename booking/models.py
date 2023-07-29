import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Booking(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    num_guests = models.PositiveIntegerField(default=0)
    checked_guests = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)


    # Add more fields as per your application's requirements

    def __str__(self):
        return f"{self.uuid}"


class Table(models.Model):
    number_of_seats = models.IntegerField()
    full_price = models.FloatField()
    deposit = models.FloatField()
    name = models.CharField(max_length=32)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='tables')

    def __str__(self):
        return f"{self.name}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Add more fields as per your application's requirements

    def __str__(self):
        return f"Booking: {self.booking} - Amount: {self.amount}"
