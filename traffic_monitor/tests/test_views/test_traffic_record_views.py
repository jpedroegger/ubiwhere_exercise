import pytest
from traffic_monitor.models import TrafficRecord
import datetime
from django.conf import settings
from django.utils import timezone


@pytest.mark.django_db
def test_get_traffic_record_list_view(api_client, super_user, sample_traffic_record):

    api_client.force_authenticate(user=super_user)

    read_response = api_client.get(
        "/api/traffic_records/",
        format="json",
    )

    assert read_response.status_code == 200
    assert read_response.data["count"] == 1


@pytest.mark.django_db
def test_get_traffic_record_list_view_without_credentials(
    api_client, sample_traffic_record
):

    read_response = api_client.get(
        "/api/traffic_records/",
        format="json",
    )

    assert read_response.status_code == 403


@pytest.mark.django_db
def test_get_traffic_record_filtered_list(
    api_client,
    super_user,
    sample_traffic_record,
    sample_road_segment,
    sample_sensor,
    sample_car,
):

    api_client.force_authenticate(user=super_user)

    date_range = timezone.now() - datetime.timedelta(days=6)

    TrafficRecord.objects.create(
        timestamp=date_range,
        road_segment=sample_road_segment,
        sensor=sample_sensor,
        car=sample_car,
    )

    read_response = api_client.get(
        "/api/traffic_records/?license_plate=AA00AA",
        format="json",
    )

    assert read_response.status_code == 200
    assert read_response.data["count"] == 1


@pytest.mark.django_db
def test_traffic_record_create_view(
    api_client,
    super_user,
    traffic_record_list_payload,
    sample_road_segment,
    sample_sensor,
):

    api_client.credentials(HTTP_AUTHORIZATION=f"API-Key {settings.API_KEY}")

    create_response = api_client.post(
        "/api/traffic_records/", data=traffic_record_list_payload, format="json"
    )

    assert create_response.status_code == 201

    api_client.force_authenticate(user=super_user)

    read_response = api_client.get(
        "/api/traffic_records/",
        format="json",
    )

    assert read_response.data["count"] == 2


@pytest.mark.django_db
def test_traffic_record_accepts_only_lists(
    api_client, sample_road_segment, sample_sensor
):

    api_client.credentials(HTTP_AUTHORIZATION=f"API-Key {settings.API_KEY}")

    create_response = api_client.post(
        "/api/traffic_records/",
        data={
            "road_segment": sample_road_segment.id,
            "car__license_plate": "AA00AA",
            "timestamp": "2023-05-29T17:05:21.713Z",
            "sensor__uuid": sample_sensor.uuid,
        },
        format="json",
    )
    assert create_response.status_code == 400


@pytest.mark.django_db
def test_traffic_record_create_view_without_APIKey(
    api_client, traffic_record_list_payload
):

    create_response = api_client.post(
        "/api/traffic_records/", data=traffic_record_list_payload, format="json"
    )

    assert create_response.status_code == 403
    assert create_response.data == {
        "detail": "Authentication credentials were not provided."
    }


@pytest.mark.django_db
def test_traffic_record_create_only_valid_inputs(
    api_client, sample_road_segment, sample_sensor
):

    api_client.credentials(HTTP_AUTHORIZATION=f"API-Key {settings.API_KEY}")

    payload = [
        {
            "road_segment": sample_road_segment.id,
            "car__license_plate": "AA00AA",
            "timestamp": timezone.now(),
            "sensor__uuid": str(sample_sensor.uuid),
        },
        {
            "car__license_plate": "AA00AA",
            "timestamp": timezone.now(),
            "sensor__uuid": str(sample_sensor.uuid),
        },
        {
            "road_segment": sample_road_segment.id,
            "car__license_plate": "CC00CC",
            "timestamp": timezone.now(),
        },
        {
            "road_segment": sample_road_segment.id,
            "timestamp": timezone.now(),
            "sensor__uuid": str(sample_sensor.uuid),
        },
    ]

    response = api_client.post("/api/traffic_records/", payload, format="json")

    assert response.status_code == 201
    assert "invalid_inputs" in response.data
    assert len(response.data["data"]) == 1
    assert len(response.data["invalid_inputs"]) == 3


@pytest.mark.django_db
def test_create_traffic_records_all_invalid(api_client):

    api_client.credentials(HTTP_AUTHORIZATION=f"API-Key {settings.API_KEY}")

    payload = [
        {"car__license_plate": "AA00AA"},
        {"sensor__uuid": "some-uuid"},
        {"road_segment": 1},
    ]

    response = api_client.post("/api/traffic_records/", payload, format="json")

    (f"\nDATA: {response.data}\n")
    assert response.status_code == 201
    assert len(response.data["invalid_inputs"]) == 3
    assert len(response.data["data"]) == 0
