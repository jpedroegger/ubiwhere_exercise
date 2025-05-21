from django.db import models
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import LineString


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
    road_length = models.DecimalField(max_digits=13, decimal_places=9)

    @classmethod
    def has_duplicate_linestring(cls, linestring):
        """
        Check if a linestring already exists in the database.
        """
        new_coordinate = list(linestring.coords)

        return cls.objects.filter(
            models.Q(coordinate__exact=linestring) |
            models.Q(coordinate__exact=LineString(new_coordinate[::-1]))
        ).exists()
    
    def clean(self):
        """
        Method to call custom validation before saving.
        """
        if self.coordinate and self.has_duplicate_linestring(self.coordinate):
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