from rest_framework import serializers

from .serializers import BookingOutputSerializer


class UserBookingSchema(serializers.Serializer):
    active_bookings = BookingOutputSerializer()
    past_bookings = BookingOutputSerializer()
