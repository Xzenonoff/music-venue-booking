from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet

router_v1 = DefaultRouter(trailing_slash=False)
router_v1.register("booking", BookingViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
]
