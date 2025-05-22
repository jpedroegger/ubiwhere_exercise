from traffic_monitor.models import RoadSegment, SpeedReading
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.geos import LineString


class RoadSegmentSerializer(GeoFeatureModelSerializer):
    speed_records = serializers.SerializerMethodField()
    traffic_classification = serializers.SerializerMethodField()
    coordinate = GeometryField()

    class Meta:
        model = RoadSegment
        fields = '__all__'
        geo_field = 'coordinate'

    def validate_coordinate(self, value):
        instance_id = self.instance.id if self.instance else None

        if RoadSegment.objects.duplicate_exists(value, exclude_id=instance_id):
            raise serializers.ValidationError(
                "A road segment with these coordinates already exists."
            )
        
        return value

    def get_speed_records(self, obj):
        return obj.speed_readings.count()
    
    def get_traffic_classification(self, obj):
        classification = obj.current_speed_classification()
        return classification.name if classification else None


class SpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedReading
        fields = '__all__'