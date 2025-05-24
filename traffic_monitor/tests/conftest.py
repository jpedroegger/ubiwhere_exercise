import pytest
import datetime
from traffic_monitor.models import (
    TrafficClassification, RoadSegment, SpeedReading, TrafficRecord, Sensor, Car)
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import LineString
from rest_framework.test import APIClient
from django.utils import timezone



@pytest.fixture
def api_client():
    yield APIClient()

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="testuser@test.com"
    )

@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        username="test_admin",
        password="test_admin",
        email="test_admin@admin.com"
    )

@pytest.fixture
def line_string():
    return LineString((104.1119814, 30.653166), (104.110012, 30.64971387))


@pytest.fixture
def reversed_line_string():
    return LineString((104.110012, 30.64971387), (104.1119814, 30.653166))

@pytest.fixture
def traffic_classifications():
    return [
        TrafficClassification.objects.create(
            name='LOW',
            min_speed=0,
            max_speed=20
        ),
        TrafficClassification.objects.create(
            name='MEDIUM',
            min_speed=21,
            max_speed=50
        ),
        TrafficClassification.objects.create(
            name='HIGH',
            min_speed=51,
            max_speed=None
        )
    ]

@pytest.fixture
def sample_road_segment(line_string):
    return RoadSegment.objects.create(
        coordinate=line_string,
        road_length=100.0
    )


@pytest.fixture
def sample_speed_readings(sample_road_segment):
    return [
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=25.0,
        ),
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=45.0,
        ),
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=75.0,
        )
    ]

@pytest.fixture
def sample_speed_reading(sample_road_segment):
    return SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=25.0,
        )

@pytest.fixture
def road_segment_payload():
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [104.1119814, 30.653166],
                [104.110012, 30.64971387]
            ]
        },
        "properties": {
            "road_length": 397.8707718
        }
    }

@pytest.fixture
def road_segment_update_payload():
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [999.999999, 888.9999999],
                [889.888888, 99.88888888]
            ]
        },
        "properties": {
            "road_length": 99.99
        }
    }

@pytest.fixture
def sample_sensor():
    return Sensor.objects.create(
        id=99,
        name="Test Sensor",
        uuid="2fad650b-de67-48c5-bb0c-0d6eb02e8499",
    )

@pytest.fixture
def sample_car():
    return Car.objects.create(
        license_plate="AA00AA",
    )

@pytest.fixture
def sample_traffic_record(sample_road_segment, sample_sensor, sample_car):
    return TrafficRecord.objects.create(
        road_segment=sample_road_segment,
        sensor=sample_sensor,
        car=sample_car,
        timestamp=timezone.now(),
    )

@pytest.fixture
def traffic_record_list_payload(sample_road_segment, sample_sensor):
    return [
        {
            "road_segment" : sample_road_segment.id,
            "car__license_plate":"AA00AA",
            "timestamp": "2023-05-29T17:05:21.713Z",
            "sensor__uuid": sample_sensor.uuid
        },
        {
            "road_segment" : sample_road_segment.id,
            "car__license_plate":"BB11BB",
            "timestamp": "2025-05-22T17:05:21.713Z",
            "sensor__uuid":  sample_sensor.uuid
        }
    ]
