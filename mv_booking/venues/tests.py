from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AvailabilitySchedule, MusicVenue
from .serializers import AvailabilityScheduleSerializer


class MusicVenueViewSetTestCase(APITestCase):
    def setUp(self):
        self.music_venue = MusicVenue.objects.create(
            name="Venue1",
            address="123 Street",
            sound_equipment=True,
            stage=True,
            lighting=True,
        )
        self.schedule = AvailabilitySchedule.objects.create(
            venue=self.music_venue,
            date=datetime.strptime("01-01-2024", "%d-%m-%Y").date(),
            opening_time="10:00:00",
            closing_time="18:00:00",
        )
        self.url = reverse("musicvenue-schedules", kwargs={"pk": self.music_venue.pk})

    def test_list_schedules(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = AvailabilityScheduleSerializer(instance=self.schedule).data
        self.assertIn(serializer_data, response.data)

    def test_create_schedule(self):
        new_schedule_data = {
            "venue_id": self.music_venue.pk,
            "date": "31-12-2024",
            "opening_time": "09:00:00",
            "closing_time": "17:00:00",
        }

        response = self.client.post(self.url, new_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(AvailabilitySchedule.objects.count(), 2)

    def test_retrieve_schedule(self):
        schedule_detail_url = reverse(
            "musicvenue-schedule",
            kwargs={"pk": self.music_venue.pk, "schedule_id": self.schedule.pk},
        )

        response = self.client.get(schedule_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = AvailabilityScheduleSerializer(instance=self.schedule).data
        self.assertEqual(response.data, serializer_data)

    def test_update_schedule(self):
        schedule_detail_url = reverse(
            "musicvenue-schedule",
            kwargs={"pk": self.music_venue.pk, "schedule_id": self.schedule.pk},
        )
        updated_data = {
            "date": "01-01-2024",
            "opening_time": "08:00:00",
            "closing_time": "16:00:00",
        }

        response = self.client.put(schedule_detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.date.strftime("%d-%m-%Y"), updated_data["date"])

        self.assertEqual(
            self.schedule.opening_time.strftime("%H:%M:%S"),
            updated_data["opening_time"],
        )

        self.assertEqual(
            self.schedule.closing_time.strftime("%H:%M:%S"),
            updated_data["closing_time"],
        )

    def test_delete_schedule(self):
        schedule_detail_url = reverse(
            "musicvenue-schedule",
            kwargs={"pk": self.music_venue.pk, "schedule_id": self.schedule.pk},
        )

        response = self.client.delete(schedule_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AvailabilitySchedule.objects.filter(pk=self.schedule.pk).exists()
        )
