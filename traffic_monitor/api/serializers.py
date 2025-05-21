from traffic_monitor.models import RoadSegment, SpeedReading
from rest_framework import serializers


class RoadSegmentSerializer(serializers.ModelSerializer):
    speed_records = serializers.SerializerMethodField()
    class Meta:
        model = RoadSegment
        fields = '__all__'

    def get_speed_records(self, obj):
        return obj.speed_readings.count()


class SpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedReading
        fields = '__all__'