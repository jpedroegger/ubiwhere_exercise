from django.db.models import OuterRef, Subquery
from rest_framework import generics
from traffic_monitor.models import RoadSegment, SpeedReading, TrafficClassification
from traffic_monitor.api.serializers import RoadSegmentSerializer, SpeedReadingSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class RoadSegmentListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    queryset = RoadSegment.objects.none()
    serializer_class = RoadSegmentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        classification_filter = self.request.query_params.get('classification', None)
        
        if not classification_filter:
            return RoadSegment.objects.all()

        try:
            classification = TrafficClassification.objects.get(name=classification_filter.upper())
        except TrafficClassification.DoesNotExist:
            return RoadSegment.objects.none()
        latest_readings = SpeedReading.objects.filter(
            road_segment=OuterRef('pk')
        ).order_by('-created_at')
        
        return RoadSegment.objects.annotate(
            latest_speed=Subquery(latest_readings.values('speed')[:1])
        ).filter(
            latest_speed__gte=classification.min_speed or 0,
            latest_speed__lte=classification.max_speed or float('inf')
        )


class RoadSegmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a roada segment.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class SpeedReadingListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class SpeedReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a roada segment.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
