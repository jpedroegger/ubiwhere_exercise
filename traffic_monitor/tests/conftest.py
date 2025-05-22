import pytest
from traffic_monitor.models import TrafficClassification, RoadSegment, SpeedReading
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import LineString
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient


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
    """Returns a basic RoadSegment instance"""
    return RoadSegment.objects.create(
        coordinate=line_string,
        road_length=100.0
    )


@pytest.fixture
def sample_speed_readings(sample_road_segment):
    now = timezone.now()
    return [
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=25.0,
            created_at=now - timedelta(days=2)
        ),
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=45.0,
            created_at=now - timedelta(days=1)
        ),
        SpeedReading.objects.create(
            road_segment=sample_road_segment,
            speed=75.0,
            created_at=now
        )
    ]

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