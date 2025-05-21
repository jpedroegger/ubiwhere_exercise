from django.db.models import Prefetch
from rest_framework import generics
from traffic_monitor.models import RoadSegment, SpeedReading
from traffic_monitor.api.serializers import RoadSegmentSerializer, SpeedReadingSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class RoadSegmentListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    # queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        classification_filter = self.request.query_params.get('classification', None)
        latest_readings = SpeedReading.objects.order_by('-created_at')

        segments = RoadSegment.objects.prefetch_related(
            Prefetch('speed_readings', queryset=latest_readings, to_attr='all_readings')
        )

        if classification_filter:
            classification_filter = classification_filter.upper()
            filtered = []

            for segment in segments:
                if segment.all_readings:
                    latest = segment.all_readings[0]
                    if latest.classification and latest.classification.name == classification_filter:
                        filtered.append(segment)

            return filtered

        return segments


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
