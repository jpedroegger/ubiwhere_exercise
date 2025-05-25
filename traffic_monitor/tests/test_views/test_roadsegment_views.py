import pytest
from traffic_monitor.models import RoadSegment, SpeedReading
from django.contrib.gis.geos import LineString


@pytest.mark.django_db
def test_get_road_segment_list(api_client, sample_road_segment):

    RoadSegment.objects.create(
        coordinate=LineString((104.110012, 31.64971387), (104.1119814, 31.653166)),
        road_length=100.0,
    )

    response_read = api_client.get("/api/road_segments/", format="json")

    assert response_read.status_code == 200
    assert response_read.data["count"] == 2


@pytest.mark.django_db
def test_get_road_segment_list_with_filter(
    api_client, sample_road_segment, sample_speed_readings
):

    low_classified_road_segment = RoadSegment.objects.create(
        coordinate=LineString((104.110012, 31.64971387), (104.1119814, 31.653166)),
        road_length=100.0,
    )
    SpeedReading.objects.create(
        road_segment=low_classified_road_segment,
        speed=100.0,
    )

    medium_classified_road_segment = RoadSegment.objects.create(
        coordinate=LineString((104.110012, 31.64971387), (104.1119814, 31.653160)),
        road_length=100.0,
    )
    SpeedReading.objects.create(
        road_segment=medium_classified_road_segment,
        speed=40.0,
    )

    response_read = api_client.get(
        "/api/road_segments/?classification=LOW", format="json"
    )

    assert response_read.status_code == 200
    assert response_read.data["count"] == 2


@pytest.mark.django_db
def test_create_road_segment(api_client, super_user):

    api_client.force_authenticate(user=super_user)

    response_create = api_client.post(
        "/api/road_segments/",
        data={
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[104.1119814, 30.653166], [104.110012, 30.64971387]],
            },
            "properties": {"road_length": 397.8707718},
        },
        format="json",
    )

    assert response_create.status_code == 201
    assert response_create.data["geometry"]["coordinates"] == list(
        [[104.1119814, 30.653166], [104.110012, 30.64971387]]
    )
    assert response_create.data["properties"]["road_length"] == 397.8707718


@pytest.mark.django_db
def test_create_road_segment_without_credentials(
    api_client, user, road_segment_payload
):

    api_client.force_authenticate(user=user)

    response_create = api_client.post(
        "/api/road_segments/", data=road_segment_payload, format="json"
    )

    assert response_create.status_code == 403
    assert (
        response_create.data["detail"]
        == "You do not have permission to perform this action."
    )

    response_read = api_client.get("/api/road_segments/", format="json")
    assert response_read.data["count"] == 0


####################################DetailView########################################


### GET
@pytest.mark.django_db
def test_get_road_segment_detail(api_client, sample_road_segment, line_string):

    valid_response_read = api_client.get(
        f"/api/road_segments/{sample_road_segment.id}/", format="json"
    )

    response_coordinates = valid_response_read.data["geometry"]["coordinates"]
    response_line_string = LineString(response_coordinates)

    assert valid_response_read.status_code == 200
    assert response_line_string.equals_exact(line_string)

    road_length = valid_response_read.data["properties"]["road_length"]
    assert road_length == 100.0

    invalid_response_read = api_client.get(f"/api/road_segments/11111/", format="json")
    assert invalid_response_read.status_code == 404


##### PUT
@pytest.mark.django_db
def test_update_road_segment(
    api_client, super_user, sample_road_segment, road_segment_update_payload
):

    api_client.force_authenticate(user=super_user)

    response_update = api_client.put(
        f"/api/road_segments/{sample_road_segment.id}/",
        data=road_segment_update_payload,
        format="json",
    )

    assert response_update.status_code == 200

    response_read = api_client.get(
        f"/api/road_segments/{sample_road_segment.id}/", format="json"
    )

    assert response_read.status_code == 200
    assert response_read.data["geometry"]["coordinates"] == list(
        [[999.999999, 888.9999999], [889.888888, 99.88888888]]
    )
    assert response_read.data["properties"]["road_length"] == 99.99


@pytest.mark.django_db
def test_incomplete_update_road_segment(api_client, super_user, sample_road_segment):

    api_client.force_authenticate(user=super_user)

    response_update = api_client.put(
        f"/api/road_segments/{sample_road_segment.id}/",
        data={
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[999.999999, 888.9999999], [889.888888, 99.88888888]],
            },
            "properties": {},
        },
        format="json",
    )

    assert response_update.status_code == 400


@pytest.mark.django_db
def test_update_road_segment_without_credenticals(
    api_client, user, sample_road_segment, road_segment_update_payload
):

    api_client.force_authenticate(user=user)

    response_update = api_client.put(
        f"/api/road_segments/{sample_road_segment.id}/",
        data=road_segment_update_payload,
        format="json",
    )

    assert response_update.status_code == 403
    assert (
        response_update.data["detail"]
        == "You do not have permission to perform this action."
    )


##### PATCH
@pytest.mark.django_db
def test_partial_update_road_segment(api_client, super_user, sample_road_segment):

    api_client.force_authenticate(user=super_user)

    response_update = api_client.patch(
        f"/api/road_segments/{sample_road_segment.id}/",
        data={"type": "Feature", "properties": {"road_length": 10.0}},
        format="json",
    )

    assert response_update.status_code == 200

    response_read = api_client.get(
        f"/api/road_segments/{sample_road_segment.id}/", format="json"
    )

    assert response_read.status_code == 200
    assert response_read.data["geometry"]["coordinates"] == list(
        [[104.1119814, 30.653166], [104.110012, 30.64971387]]
    )
    assert response_read.data["properties"]["road_length"] == 10.0


@pytest.mark.django_db
def test_partial_update_road_segment_without_credentials(
    api_client, user, sample_road_segment, road_segment_update_payload
):

    api_client.force_authenticate(user=user)

    response_update = api_client.patch(
        f"/api/road_segments/{sample_road_segment.id}/",
        data=road_segment_update_payload,
        format="json",
    )

    assert response_update.status_code == 403
    assert (
        response_update.data["detail"]
        == "You do not have permission to perform this action."
    )


### DELETE
@pytest.mark.django_db
def test_delete_road_segment(api_client, super_user, sample_road_segment):

    api_client.force_authenticate(user=super_user)

    response_before_delete = api_client.get(
        f"/api/road_segments/{sample_road_segment.id}/", format="json"
    )

    assert response_before_delete.status_code == 200

    response_delete = api_client.delete(f"/api/road_segments/{sample_road_segment.id}/")

    assert response_delete.status_code == 204

    response_after_read = api_client.get(
        f"/api/road_segments/{sample_road_segment.id}/"
    )

    assert response_after_read.status_code == 404


@pytest.mark.django_db
def test_delete_road_segment_without_credentials(api_client, user, sample_road_segment):

    api_client.force_authenticate(user=user)

    response_delete = api_client.delete(f"/api/road_segments/{sample_road_segment.id}/")

    assert response_delete.status_code == 403
    assert (
        response_delete.data["detail"]
        == "You do not have permission to perform this action."
    )
