import django_filters
from django.db.models import OuterRef, Subquery, Count
from traffic_monitor.models import RoadSegment, SpeedReading, TrafficClassification


class RoadSegmentFilter(django_filters.FilterSet):
    classification = django_filters.CharFilter(method="filter_by_classification")

    class Meta:
        model = RoadSegment
        fields = []

    def filter_by_classification(self, queryset, name, value):
        value = value.upper()
        try:
            classification = TrafficClassification.objects.get(name=value)
        except TrafficClassification.DoesNotExist:
            return queryset.none()

        latest_speed_subquery = (
            SpeedReading.objects.filter(road_segment=OuterRef("pk"))
            .order_by("-created_at")
            .values("speed")[:1]
        )

        queryset = queryset.annotate(
            latest_speed=Subquery(latest_speed_subquery),
            speed_reading_count=Count("speed_readings"),
        ).prefetch_related("speed_readings")

        min_speed = classification.min_speed or 0
        max_speed = classification.max_speed or float("inf")
        return queryset.filter(latest_speed__gte=min_speed, latest_speed__lte=max_speed)
