import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import LineString
from traffic_monitor.models import RoadSegment, SpeedReading
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Import road segments and speed readings from CSV file'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('./traffic_speed.csv')

        speed_readings = []
        CHUNK_SIZE = 1000
        for index, row in df.iterrows():
            try:
                # Extract coordinates from row
                start_point = (float(row['Long_start']), float(row['Lat_start']))
                end_point = (float(row['Long_end']), float(row['Lat_end']))
                coords = [start_point, end_point]
                reverse_coords = [end_point, start_point]

                line = LineString(coords)
                reverse_line = LineString(reverse_coords)

                # Check if segment already exists in either direction
                road = RoadSegment.objects.filter(coordinate__equals=line).first()
                if not road:
                    road = RoadSegment.objects.filter(coordinate__equals=reverse_line).first()

                if not road:
                    road = RoadSegment.objects.create(
                        coordinate=line,
                        road_length=Decimal(row['Length'])
                    )

                speed = float(row['Speed'])
                speed_readings.append(SpeedReading(
                    road_segment=road,
                    speed=speed,
                    created_at=timezone.now()
                ))

                # Bulk insert in chunks
                if len(speed_readings) >= CHUNK_SIZE:
                    SpeedReading.objects.bulk_create(speed_readings)
                    speed_readings.clear()

            except Exception as e:
                self.stderr.write(f"Skipping row {index} due to error: {e}")

        if speed_readings:
            SpeedReading.objects.bulk_create(speed_readings)

        self.stdout.write(self.style.SUCCESS("Import completed."))
