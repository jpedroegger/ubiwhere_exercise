from traffic_monitor.models import RoadSegment, SpeedReading
from rest_framework import serializers


class RoadSegmentSerializer(serializers.ModelSerializer):
    speed_records = serializers.SerializerMethodField()
    traffic_classification = serializers.SerializerMethodField()
    class Meta:
        model = RoadSegment
        fields = '__all__'

    def get_speed_records(self, obj):
        return obj.speed_readings.count()
    
    def get_traffic_classification(self, obj):
        classification = obj.current_speed_classification()
        return classification.name if classification else None


class SpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedReading
        fields = '__all__'