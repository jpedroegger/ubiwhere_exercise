from traffic_monitor.models import RoadSegment, SpeedReading
from rest_framework import serializers


class RoadSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSegment
        fields = '__all__'


class SpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedReading
        fields = '__all__'