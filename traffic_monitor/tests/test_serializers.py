import pytest
from traffic_monitor.api.serializers import (
    RoadSegmentSerializer,
    SpeedReadingSerializer,
)
from traffic_monitor.models import RoadSegment, SpeedReading
from django.contrib.gis.geos import LineString
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_road_segment_serializer_valid(road_segment_payload):

    data = road_segment_payload
    serializer = RoadSegmentSerializer(data=data)

    assert serializer.is_valid()
    road_segment = serializer.save()
    assert road_segment.road_length == 397.8707718


@pytest.mark.django_db
def test_road_segment_serializer_duplicate():
    RoadSegment.objects.create(
        coordinate=LineString([(1.0, 2.0), (3.0, 4.0)]), road_length=1000.0
    )
    duplicate = {
        "coordinate": {"type": "LineString", "coordinates": [(3.0, 4.0), (1.0, 2.0)]},
        "road_length": 900.0,
    }
    serializer = RoadSegmentSerializer(data=duplicate)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)
    assert "already exists" in str(e.value)


@pytest.mark.django_db
def test_road_segment_returns_correct_speed_records_count(
    sample_road_segment, sample_speed_readings
):
    serializer = RoadSegmentSerializer(instance=sample_road_segment)

    assert serializer.data["properties"]["speed_records"] == 3


@pytest.mark.django_db
def test_road_segment_returns_correct_classification(
    sample_road_segment, sample_speed_readings
):
    SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=55.0,
    )

    serializer = RoadSegmentSerializer(instance=sample_road_segment)
    assert serializer.data["properties"]["traffic_classification"] == "LOW"

    SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=10.0,
    )

    serializer = RoadSegmentSerializer(instance=sample_road_segment)
    assert serializer.data["properties"]["traffic_classification"] == "HIGH"


@pytest.mark.django_db
def test_speed_readings_serializer_valid(sample_road_segment):

    data = {"speed": 88.8, "road_segment": sample_road_segment.id}
    serializer = SpeedReadingSerializer(data=data)

    assert serializer.is_valid()
    speed_readings = serializer.save()
    assert speed_readings.speed == 88.8


@pytest.mark.django_db
def test_speed_reading_serializer_create(sample_road_segment):
    data = {"speed": 88.8, "road_segment": sample_road_segment.id}
    serializer = SpeedReadingSerializer(data=data)
    assert serializer.is_valid()
    speed_reading = serializer.save()
    assert speed_reading.speed == 88.8
    assert speed_reading.road_segment == sample_road_segment
