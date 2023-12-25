from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ("user", "booking_date", "venue")
    list_display = ("user", "booking_date", "venue", "is_cancelled")
    search_fields = ("user", "booking_date", "venue")
    autocomplete_fields = (
        "user",
        "venue",
    )
