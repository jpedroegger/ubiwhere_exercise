from traffic_monitor.models import Car, Sensor
from traffic_monitor.api.serializers import CarSerializer, SensorSerializer
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

def get_or_create_car_dict(license_plates: set) -> dict:

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
    
    sensors = {}

    for uuid in sensor_uuids:
        try:
            UUID(str(uuid))
            sensor = Sensor.objects.get(uuid=uuid)
            sensors[str(uuid)] = sensor
        except ValueError:
            sensors[str(uuid)] = None
    return sensors
