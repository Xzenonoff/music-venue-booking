# Generated by Django 5.0 on 2023-12-24 09:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("venues", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                ("start_time", models.DateTimeField(verbose_name="Время начала брони")),
                (
                    "end_time",
                    models.DateTimeField(verbose_name="Время окончания брони"),
                ),
                ("booking_date", models.DateField(verbose_name="День брониривания")),
                (
                    "contact_info",
                    models.CharField(max_length=255, verbose_name="Контактные данные"),
                ),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "venue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="venues.musicvenue",
                        verbose_name="Площадка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Бронь",
                "verbose_name_plural": "Брони",
                "ordering": ("venue", "booking_date"),
            },
        ),
    ]
