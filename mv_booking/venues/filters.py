import django_filters

from .models import MusicVenue


class MusicVenueFilter(django_filters.FilterSet):
    sound_equipment = django_filters.BooleanFilter(field_name="sound_equipment")
    stage = django_filters.BooleanFilter(field_name="stage")
    lighting = django_filters.BooleanFilter(field_name="lighting")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    address = django_filters.CharFilter(field_name="address", lookup_expr="icontains")
    availability_date = django_filters.DateFilter(
        field_name="availability__date", lookup_expr="exact"
    )

    class Meta:
        model = MusicVenue
        fields = ["sound_equipment", "stage", "lighting", "name", "address"]
