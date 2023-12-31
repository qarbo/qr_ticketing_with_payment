# Generated by Django 4.2.3 on 2023-08-18 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_booking_selected_option"),
    ]

    operations = [
        migrations.CreateModel(
            name="CheckIn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("guests_checked_in", models.PositiveIntegerField(default=0)),
                ("checkin_time", models.DateTimeField(auto_now_add=True)),
                (
                    "booking",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="checkins",
                        to="booking.booking",
                    ),
                ),
            ],
        ),
    ]
