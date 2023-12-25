from django.contrib.auth import get_user_model
from django.db import models

from venues.models import MusicVenue

User = get_user_model()


class Booking(models.Model):
    venue = models.ForeignKey(
        MusicVenue,
        verbose_name="Площадка",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    start_time = models.TimeField("Время начала брони")
    end_time = models.TimeField("Время окончания брони")
    booking_date = models.DateField("День брониривания")
    contact_info = models.CharField("Контактные данные", max_length=255)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = (
            "venue",
            "booking_date",
        )

    def __str__(self):
        return f"{self.venue.name} {self.booking_date}"
