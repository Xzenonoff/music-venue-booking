from django.db import models


class MusicVenue(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)
    address = models.CharField("Адрес", max_length=255)
    sound_equipment = models.BooleanField("Оборудование", default=False)
    stage = models.BooleanField("Сцена", default=False)
    lighting = models.BooleanField("Освещение", default=False)

    class Meta:
        verbose_name = "Музыкальная площадка"
        verbose_name_plural = "Музыкальные площадки"
        ordering = ("name",)

    def __str__(self):
        return self.name


class AvailabilitySchedule(models.Model):
    venue = models.ForeignKey(
        MusicVenue,
        verbose_name="Площадка",
        on_delete=models.CASCADE,
        related_name="availability",
    )
    date = models.DateField("Дата")
    opening_time = models.TimeField("Время открытия")
    closing_time = models.TimeField("Время закрытия")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "date"], name="venue_date_constraint"
            )
        ]
        verbose_name = "График доступности"
        verbose_name_plural = "Графики доступности"
        ordering = ("venue",)

    def __str__(self):
        return self.venue.name
