import pytest
from django.contrib.gis.geos import LineString
from traffic_monitor.models import TrafficClassification, RoadSegment, SpeedReading
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_duplicate_detection_excludes_given_id(line_string, sample_road_segment):

    assert RoadSegment.objects.duplicate_exists(
        line_string, 
        exclude_id=sample_road_segment.id) is False


@pytest.mark.django_db
def test_traffic_classification_creation():
    classification = TrafficClassification.objects.create(
        name='MEDIUM',
        min_speed=31,
        max_speed=60
    )
    
    assert classification.get_name_display() == 'medium'
    assert classification.min_speed == 31
    assert classification.max_speed == 60
    assert str(classification) == "medium (31 a 60)"


@pytest.mark.django_db
def test_road_segment_creation(line_string):
    road_segment = RoadSegment.objects.create(
        coordinate=line_string,
        road_length=1179.207157
    )
    
    assert road_segment.road_length == 1179.207157
    assert road_segment.coordinate.equals(line_string)


@pytest.mark.django_db
def test_road_segment_duplicate_detection(line_string, reversed_line_string):
    RoadSegment.objects.create(
        coordinate=line_string,
        road_length=1179.207157
    )

    assert RoadSegment.objects.duplicate_exists(line_string) is True
    assert RoadSegment.objects.duplicate_exists(reversed_line_string) is True
    assert RoadSegment.objects.count() == 1

    new_line_string = LineString(
        (999.999999, 888.9999999),
        (889.888888, 99.88888888)
    )
    assert RoadSegment.objects.duplicate_exists(new_line_string) is False


@pytest.mark.django_db
def test_clean_method_raises_validation_error(line_string):
    RoadSegment.objects.create(
        coordinate=line_string,
        road_length=1179.207157
    )

    duplicated_road_segment = RoadSegment(
        coordinate=line_string,
        road_length=1179.207150
    )

    with pytest.raises(ValidationError) as e:
        duplicated_road_segment.clean()

    assert 'A road segment with these coordinates already exists.' in str(e.value)


@pytest.mark.django_db
def test_save_method_calls_validation(line_string):
    RoadSegment.objects.create(
        coordinate=line_string,
        road_length=1179.207157
    )

    duplicated_road_segment = RoadSegment(
        coordinate=line_string,
        road_length=1179.207150
    )


    with pytest.raises(ValidationError) as e:
        duplicated_road_segment.save()

    assert 'A road segment with these coordinates already exists.' in str(e.value)


@pytest.mark.django_db
def test_speed_reading_creation(sample_road_segment):
    speed_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=55.0
    )

    assert speed_reading.speed == 55.0
    assert str(speed_reading) == f"SpeedReading-> RoadSegment:{sample_road_segment.id} at speed:55.0)"


@pytest.mark.django_db
def test_current_speed_classification_empty(sample_road_segment):
    assert sample_road_segment.current_speed_classification() is None

@pytest.mark.django_db
def test_current_speed_classification_with_readings(sample_road_segment, sample_speed_readings, traffic_classifications):
    classification = sample_road_segment.current_speed_classification()
    
    assert classification is not None
    assert classification.name == 'HIGH'

@pytest.mark.django_db
def test_current_speed_classification_returns_last_reading(sample_road_segment, sample_speed_readings, traffic_classifications):
    SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=11.0,
    )

    assert sample_road_segment.current_speed_classification().name == 'LOW'

@pytest.mark.django_db
def test_speed_reading_classification_property(sample_road_segment, traffic_classifications):

    low_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=11.0 
    )
    assert low_reading.classification.name == 'LOW'
    
    medium_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=45.0 
    )
    assert medium_reading.classification.name == 'MEDIUM'
    
    high_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=75.0 
    )
    assert high_reading.classification.name == 'HIGH'

    boundary_reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=51.0 
    )
    assert boundary_reading.classification.name == 'HIGH' 

@pytest.mark.django_db
def test_speed_reading_classification_no_match(sample_road_segment):
    reading = SpeedReading.objects.create(
        road_segment=sample_road_segment,
        speed=-10.0
    )
    assert reading.classification is None