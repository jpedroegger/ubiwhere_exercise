from traffic_monitor.models import Car, Sensor
from traffic_monitor.api.serializers import CarSerializer, SensorSerializer
from uuid import UUID


def get_or_create_car_dict(license_plates: set) -> dict:
    """
    Query the Car table filtering for license_plate.
    This functions assure the cars will be created or fetched when
    a new record is being made.
    """
    cars = {car.license_plate: car for car in Car.objects.filter(license_plate__in=license_plates)}
    
    missing_plates = license_plates - cars.keys()
    
    for plate in missing_plates:
        serializer = CarSerializer(data={"license_plate": plate})
        if serializer.is_valid():
            new_car = serializer.save()
            cars[plate] = new_car
        else:
            cars[plate] = None
    
    return cars


def get_valide_uuids(sensor_uuids: set) -> dict:
    """
    This functions assures every sensor_uuid input is a aproper UUID or returns None
    """
    sensors = {}

    for uuid in sensor_uuids:
        try:
            UUID(str(uuid))
            sensor = Sensor.objects.get(uuid=uuid)
            sensors[str(uuid)] = sensor
        except ValueError:
            sensors[str(uuid)] = None
    return sensors
