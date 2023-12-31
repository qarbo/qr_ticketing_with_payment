# Generated by Django 4.2.3 on 2023-08-01 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="selected_option",
            field=models.CharField(
                choices=[
                    ("regular_pass", "Regular pass / Стандартный вход"),
                    ("table", "Table / Бронь стола"),
                ],
                default="regular_pass",
                max_length=20,
            ),
        ),
    ]
