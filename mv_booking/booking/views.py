from datetime import date

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Booking
from .schemas import UserBookingSchema
from .serializers import BookingInputSerializer, BookingOutputSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    http_method_names = ["get", "post", "put"]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return BookingInputSerializer
        return BookingOutputSerializer

    def perform_create(self, serializer):
        venue_id = serializer.validated_data.get("venue_id")

        # Проверка, что дата и время бронирования не заняты
        if self.check_booking_overlap(venue_id, serializer.validated_data):
            raise ValidationError({"detail": "Дата и время бронирования заняты"})

        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        venue_id = instance.venue.id

        if self.check_booking_overlap(
            venue_id, serializer.validated_data, exclude_id=instance.id
        ):
            raise ValidationError("Дата и время бронирования заняты")

        serializer.save()

    @staticmethod
    def check_booking_overlap(venue_id, validated_data, exclude_id=None):
        """метод для проверки, что дата и время бронирования не заняты"""
        booking_date = validated_data.get("booking_date")
        start_time = validated_data.get("start_time")
        end_time = validated_data.get("end_time")

        bookings_overlap = Booking.objects.filter(
            Q(venue_id=venue_id)
            & Q(booking_date=booking_date)
            & (
                Q(start_time__range=(start_time, end_time))
                | Q(end_time__range=(start_time, end_time))
                | Q(start_time__lte=start_time, end_time__gte=end_time)
            )
        )

        if exclude_id:
            bookings_overlap = bookings_overlap.exclude(id=exclude_id)

        return bookings_overlap.exists()

    @swagger_auto_schema(
        methods=["POST"],
        request_body=no_body,
        responses={200: "Все бронирования отменены"},
    )
    @action(detail=True, methods=["POST"])
    def cancel_booking(self, request, pk=None):
        """Отмена брони"""
        booking = self.get_object()

        if booking.is_cancelled:
            return Response(
                {"detail": "Бронь уже отменена"}, status=status.HTTP_400_BAD_REQUEST
            )

        booking.is_cancelled = True
        booking.save()

        return Response({"detail": "Бронь отменена"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=no_body,
        responses={200: "Все бронирования отменены"},
    )
    @action(detail=False, methods=["POST"])
    def cancel_all_bookings(self, request):
        """Отмена всех броней"""
        Booking.objects.filter(is_cancelled=False).update(is_cancelled=True)
        return Response(
            {"detail": "Все бронирования отменены"}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        methods=["GET"],
        responses={
            200: openapi.Response(
                description="Список бронирований", schema=UserBookingSchema()
            )
        },
    )
    @action(detail=False, methods=["GET"])
    def user_bookings(self, request):
        """Просмотр своих активных и прошедших бронирований пользователем"""
        user = request.user

        # Получаем активные бронирования пользователя
        active_bookings = Booking.objects.filter(
            user=user,
            booking_date__gte=date.today(),
        )

        # Получаем прошедшие бронирования пользователя
        past_bookings = Booking.objects.filter(
            user=user,
            booking_date__lt=date.today(),
        )

        serializer_active = BookingOutputSerializer(active_bookings, many=True)
        serializer_past = BookingOutputSerializer(past_bookings, many=True)

        return Response(
            {
                "active_bookings": serializer_active.data,
                "past_bookings": serializer_past.data,
            },
            status=status.HTTP_200_OK,
        )
