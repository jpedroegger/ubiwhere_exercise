import pytest 
from traffic_monitor.models import RoadSegment, SpeedReading
from django.contrib.gis.geos import LineString


@pytest.mark.django_db
def test_get_speed_reading_list(api_client, sample_speed_readings):
    
    response_read = api_client.get(
        '/api/speed_readings/',
        format='json'
    )

    assert response_read.status_code == 200
    assert response_read.data['count'] == 3


@pytest.mark.django_db
def test_create_speed_reading(api_client, super_user, sample_road_segment):

    api_client.force_authenticate(user=super_user)

    response_create = api_client.post(
        '/api/speed_readings/',
        data={
            'speed': 120.0,
            'road_segment': sample_road_segment.id,
        },
        format='json'
    )

    assert response_create.status_code == 201
    assert response_create.data['speed'] == 120.0
    
    new_speed_reading_id = response_create.data['id']

    response_read = api_client.get(
        f'/api/speed_readings/{new_speed_reading_id}/'
    )

    assert response_read.status_code == 200

@pytest.mark.django_db
def test_create_speed_reading_with_invalid_data(api_client, super_user):

    api_client.force_authenticate(user=super_user)

    response_create = api_client.post(
        '/api/speed_readings/',
        data={
            'speed': 120.0,
            'road_segment': "abc",
        },
        format='json'
    )

    assert response_create.status_code == 400


@pytest.mark.django_db
def test_create_speed_reading_without_admin_credentials(api_client, user, sample_road_segment):

    api_client.force_authenticate(user=user)

    response_create = api_client.post(
        '/api/speed_readings/',
        data={
            'speed': 120.0,
            'road_segment': sample_road_segment.id,
        },
        format='json'
    )

    assert response_create.status_code == 403

    response_read = api_client.get(
        '/api/speed_readings/',
        format='json'
    )
    assert response_read.data['count'] == 0

####################################DetailView########################################

### GET
@pytest.mark.django_db
def test_get_speed_reading_detail(api_client, sample_road_segment):
 
    speed_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=25.0,
    )
    
    valid_response_read = api_client.get(
        f'/api/speed_readings/{speed_reading.id}/',
        format='json'
    ) 

    assert valid_response_read.status_code == 200
    assert valid_response_read.data['speed'] == 25.0

    invalid_response_read = api_client.get(
        f'/api/speed_readings/11111/',
        format='json'
    )
    assert invalid_response_read.status_code == 404


##### PUT
@pytest.mark.django_db
def test_update_speed_reading(api_client, super_user, sample_speed_reading, sample_road_segment):
    
    api_client.force_authenticate(user=super_user)

    response_update = api_client.put(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        data={
            'speed': 99.9,
            'road_segment': sample_road_segment.id
        }, 
        format='json'
    )

    assert response_update.status_code == 200

    response_read = api_client.get(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        format='json'
    )

    assert response_read.status_code == 200
    assert response_read.data['speed'] == 99.9


@pytest.mark.django_db
def test_incomplete_update_speed_reading(api_client, super_user, sample_speed_reading, sample_road_segment):
    
    api_client.force_authenticate(user=super_user)

    response_update = api_client.put(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        data={
            'speed': 99.9,
        }, 
        format='json'
    )

    assert response_update.status_code == 400

@pytest.mark.django_db
def test_update_speed_reading_without_credenticals(api_client, user, sample_speed_reading):
    
    api_client.force_authenticate(user=user)

    response_update = api_client.put(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        data={
            'speed': 99.9,
        }, 
        format='json'
    )

    assert response_update.status_code == 403

##### PATCH
@pytest.mark.django_db
def test_partial_update_speed_reading(api_client, super_user, sample_speed_reading):
    
    api_client.force_authenticate(user=super_user)

    response_update = api_client.patch(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        data={
            'speed': 99.9,
        },  
        format='json'
    )

    assert response_update.status_code == 200
    
    response_read = api_client.get(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        format='json'
    )
    
    assert response_read.status_code == 200
    assert response_read.data['speed'] == 99.9


@pytest.mark.django_db
def test_partial_update_speed_reading_without_credenticals(api_client, sample_speed_reading):
    
    response_update = api_client.patch(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        data={
            'speed': 99.9,
        },
        format='json'
    )

    assert response_update.status_code == 403   

### DELETE
@pytest.mark.django_db
def test_delete_speed_reading(api_client, super_user, sample_speed_reading):

    api_client.force_authenticate(user=super_user)

    response_before_delete = api_client.get(
        f'/api/speed_readings/{sample_speed_reading.id}/',
        format='json'
    )

    assert response_before_delete.status_code == 200
    
    response_delete = api_client.delete(
        f'/api/speed_readings/{sample_speed_reading.id}/')
    
    assert response_delete.status_code == 204

    response_after_read = api_client.get(
        f'/api/speed_readings/{sample_speed_reading.id}/')
    
    assert response_after_read.status_code == 404

@pytest.mark.django_db
def test_delete_speed_reading_without_credentials(api_client, sample_speed_reading):
    
    response_delete = api_client.delete(
        f'/api/speed_readings/{sample_speed_reading.id}/')
    
    assert response_delete.status_code == 403






