from datetime import date

from rest_framework import serializers

from .models import Booking


class BookingInputSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)
    venue_id = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = (
            "booking_id",
            "venue_id",
            "start_time",
            "end_time",
            "booking_date",
            "contact_info",
            "is_cancelled",
        )

    def create(self, validated_data):
        venue_id = validated_data.pop("venue_id")
        booking = Booking.objects.create(venue_id=venue_id, **validated_data)
        return booking

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        booking_date = data.get("booking_date")

        # Проверка на то, что end_time не меньше start_time
        if booking_date and booking_date < date.today():
            raise serializers.ValidationError(
                detail={"detail": "Дата бронирования не может быть раньше текущей даты"}
            )

        # проверка на то, что end_time не меньше start_time
        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError(
                detail={
                    "detail": "Время окончания брони не может быть меньше времени начала"
                }
            )

        return data


class BookingOutputSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)
    venue = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            "booking_id",
            "venue",
            "start_time",
            "end_time",
            "booking_date",
            "contact_info",
            "is_cancelled",
        )

    def get_venue(self, obj):
        return obj.venue.name
