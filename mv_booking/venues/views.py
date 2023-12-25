from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import MusicVenueFilter
from .models import AvailabilitySchedule, MusicVenue
from .serializers import AvailabilityScheduleSerializer, MusicVenueSerializer


class MusicVenueViewSet(viewsets.ModelViewSet):
    queryset = MusicVenue.objects.all()
    serializer_class = MusicVenueSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = MusicVenueFilter
    ordering_fields = ["name", "address", "sound_equipment", "stage", "lighting"]

    @action(
        detail=True,
        methods=["GET", "POST"],
        serializer_class=AvailabilityScheduleSerializer,
    )
    def schedules(self, request, pk=None):
        """Чтение и создание графиков"""
        venue = self.get_object()

        if request.method == "GET":
            availability = AvailabilitySchedule.objects.select_related("venue")
            serializer = AvailabilityScheduleSerializer(availability, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            data = self.request.data
            context = {"venue_id": venue.id}
            serializer = AvailabilityScheduleSerializer(data=data, context=context)

            if serializer.is_valid():
                serializer.save(venue_id=venue.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["GET", "PUT", "DELETE"],
        operation_id="schedule_read_update_delete",
    )
    @action(
        detail=True,
        methods=["GET", "PUT", "DELETE"],
        url_path="schedules/(?P<schedule_id>[^/.]+)",
        serializer_class=AvailabilityScheduleSerializer,
    )
    def schedule(self, request, pk=None, schedule_id=None):
        """Чтение, редактирование и удаление графика"""
        schedule = get_object_or_404(AvailabilitySchedule, id=schedule_id, venue_id=pk)

        if request.method == "GET":
            serializer = AvailabilityScheduleSerializer(schedule)
            return Response(serializer.data)

        if request.method == "PUT":
            data = self.request.data
            context = {
                "venue_id": pk,
                "date": data.get("date"),
            }
            serializer = AvailabilityScheduleSerializer(
                schedule, data=request.data, partial=True, context=context
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
