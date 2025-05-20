from rest_framework import generics
from traffic_monitor.models import RoadSegment, SpeedReading
from traffic_monitor.api.serializers import RoadSegmentSerializer, SpeedReadingSerializer


class RoadSegmentListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer


class RoadSegmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a roada segment.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer 


class SpeedReadingListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer


class SpeedReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a roada segment.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer 
