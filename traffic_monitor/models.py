from django.db import models
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import LineString
import datetime

class RoadSegmentManager(models.Manager):
    def duplicate_exists(self, linestring, exclude_id=None):
        reversed_ls = LineString(list(linestring.coords)[::-1])

        queryset = self.get_queryset().filter(
            models.Q(coordinate__exact=linestring) |
            models.Q(coordinate__exact=reversed_ls)
        )

        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)

        return queryset.exists()


class TrafficClassification(models.Model):
    
    CLASSIFICATION_CHOICES = [
        ('LOW', 'low'),
        ('MEDIUM', 'medium'),
        ('HIGH', 'high'),
    ]

    name = models.CharField(max_length=25, choices=CLASSIFICATION_CHOICES, default='LOW', unique=True)
    min_speed = models.FloatField(null=True, blank=True)
    max_speed = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['min_speed']

    def __str__(self):
        return f"{self.get_name_display()} ({self.min_speed or 'Null'} a {self.max_speed or 'Null'})"


class RoadSegment(models.Model):
    """
    Model representing a road segment.
    """
    coordinate = models.LineStringField()
    road_length = models.FloatField()

    objects = RoadSegmentManager()
    
    def clean(self):
        """
        Method to call custom validation before saving.
        """
        if self.coordinate and RoadSegment.objects.duplicate_exists(self.coordinate, exclude_id=self.id):
            raise ValidationError("A road segment with these coordinates already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def current_speed_classification(self):
        last_reading = self.speed_readings.order_by('-created_at').first()
        if last_reading:
            return last_reading.classification
        return None
    
    def __str__(self):
        return f"RoadSegment-> id:{self.id} length:{self.road_length}"


class SpeedReading(models.Model):
    """
    Model representing a speed reading for a roada segment.
    """
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='speed_readings')
    speed = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def classification(self):
        """
        Returns the classification based on actual speed rules.
        """
        try:
            return TrafficClassification.objects.filter(
                models.Q(min_speed__lte=self.speed) | models.Q(min_speed__isnull=True),
                models.Q(max_speed__gte=self.speed) | models.Q(max_speed__isnull=True),
            ).order_by('min_speed').first()
        except TrafficClassification.DoesNotExist:
            return None

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"SpeedReading-> RoadSegment:{self.road_segment.id} at speed:{self.speed})"
    

class Car(models.Model):
    """
    Model representing a car.
    """
    license_plate = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.license_plate}"
    
class Sensor(models.Model):
    """
    MOdel representing a sensor.
    """
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(unique=True, editable=False)

    def __str__(self):
        return f"{self.name}: {self.uuid}"


class TrafficRecord(models.Model):
    """
    MOdel representing a traffic record made by a sensor.
    """
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='traffic_records')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='traffic_records')
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='traffic_records')
    timestamp = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"TrafficRecord-> Sensor:{self.sensor.name} Car:{self.car.license_plate} RoadSegment:{self.road_segment.id} at {self.timestamp}"