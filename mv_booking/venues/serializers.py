from rest_framework import serializers

from .models import AvailabilitySchedule, MusicVenue


class MusicVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicVenue
        fields = (
            "id",
            "name",
            "description",
            "address",
            "sound_equipment",
            "stage",
            "lighting",
        )


class AvailabilityScheduleSerializer(serializers.ModelSerializer):
    venue = serializers.SerializerMethodField()

    class Meta:
        model = AvailabilitySchedule
        fields = (
            "id",
            "venue",
            "date",
            "opening_time",
            "closing_time",
        )

    def get_venue(self, obj):
        return obj.venue.name

    def validate(self, data):
        date = data.get("date")
        venue_id = self.context["venue_id"]
        instance = self.instance  # обновляемый объект

        if instance and "date" in data:
            # Если выполняется обновление объекта и указано новое значение date
            if (
                AvailabilitySchedule.objects.filter(venue_id=venue_id, date=date)
                .exclude(id=instance.id)
                .exists()
            ):
                raise serializers.ValidationError(
                    detail={"detail": "Запись с такой площадкой и датой уже существует"}
                )

        if not instance:
            # Если выполняется создание нового объекта (POST запрос)
            if AvailabilitySchedule.objects.filter(
                venue_id=venue_id, date=date
            ).exists():
                raise serializers.ValidationError(
                    detail={"detail": "Запись с такой площадкой и датой уже существует"}
                )

        return data
