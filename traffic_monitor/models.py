from django.db import models
from django.contrib.gis.db import models


class RoadSegment(models.Model):
    """
    Model representing a road segment.
    """
    coordinate = models.LineStringField()
    road_length = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"RoadSegment-> id:{self.id} length:{self.road_length}"

class SpeedReading(models.Model):
    """
    Model representing a speed reading for a roada segment.
    """
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='speed_readings')
    speed = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"SpeedReading-> RoadSegment:{self.road_segment.id} at speed:{self.speed})"