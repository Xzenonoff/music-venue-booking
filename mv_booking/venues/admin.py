from django.contrib import admin

from .models import AvailabilitySchedule, MusicVenue


@admin.register(MusicVenue)
class MusicVenueAdmin(admin.ModelAdmin):
    list_filter = (
        "name",
        "address",
    )
    list_display = (
        "name",
        "address",
    )
    search_fields = (
        "name",
        "address",
    )


@admin.register(AvailabilitySchedule)
class AvailabilityScheduleAdmin(admin.ModelAdmin):
    list_filter = (
        "venue",
        "date",
    )
    list_display = (
        "venue",
        "date",
        "opening_time",
        "closing_time",
    )
    search_fields = (
        "venue",
        "date",
    )
    autocomplete_fields = ("venue",)
