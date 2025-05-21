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
        if isinstance(value, dict) and value.get('type') == 'LineString':
            linestring = LineString(value['coordinates'])
        else:
            linestring = value
        
        if RoadSegment.has_duplicate_linestring(linestring):
            raise serializers.ValidationError(
                "A road segment with these coordinates already exists."
            )
        
        return linestring

    def get_speed_records(self, obj):
        return obj.speed_readings.count()
    
    def get_traffic_classification(self, obj):
        classification = obj.current_speed_classification()
        return classification.name if classification else None


class SpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedReading
        fields = '__all__'