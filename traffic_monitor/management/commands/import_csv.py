from django.core.management.base import BaseCommand
import pandas as pd
from decimal import Decimal
from django.utils import timezone
from django.contrib.gis.geos import LineString
from traffic_monitor.models import RoadSegment, SpeedReading


class Command(BaseCommand):
    """
    Custom command to import traffic_speed recods from a CSV file.
    This command reads a CSV file containing road segments and speed readings,
    and imports them into the database.
    The CSV file should have the following columns:
    - Long:start = Longitude of the start point
    - Lat_start = Latitude of the start point
    - Long_end = Longitute of the endp oint
    - Lat_end = Latitude of the endpoint
    - Length = Length of the road segment
    - Speed = Speed reading
    The command will create new RoadSegment and SpeedReading objects in the database
    avoinding duplicates by checking if the LineString already exists (even in reverse).
    It will also handle the population in chunks to avoid memory issues with large files.
    The command can be called from the command line as follows:
    python3 manage.py import_csv --file path/to/your/file.csv
    """
    help = 'Import road segments and speed readings from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            self.stderr.write(f"Could not read CSV: {e}")
            return
        
        self.import_from_dataframe(df)

    def import_from_dataframe(self, dataframe):
        """
        Handles the import logic.
        """
        CHUNK_SIZE = 1000
        buffer = []

        for index, row in dataframe.iterrows():
            try:
                road_segment = self.get_or_create_roadsegment(row)
                speed_reading = self.build_speed_reading(row, road_segment)
                buffer.append(speed_reading)

                if len(buffer) >= CHUNK_SIZE:
                    self.save_speed_readings(buffer)
                    buffer.clear()

            except Exception as e:
                self.stderr.write(f"Error at row {index}: {e}")

        if buffer: #Save remaining readings
            self.save_speed_readings(buffer)

        self.stdout.write("Import completed.")

    def get_or_create_roadsegment(self, row):
        """
        Finds or creates a RoadSegment based on LineString (and its reverse).
        """
        start_coord = (float(row['Long_start']), float(row['Lat_start']))
        end_coord = (float(row['Long_end']), float(row['Lat_end']))
        line = LineString([start_coord, end_coord])
        reversed_line = LineString([end_coord, start_coord])

        road_segment = RoadSegment.objects.filter(coordinate__equals=line).first()
        if not road_segment:
            road_segment = RoadSegment.objects.filter(coordinate__equals=reversed_line).first()
        
        if not road_segment:
            road_segment = RoadSegment.objects.create(
                coordinate=line,
                road_length=Decimal(str(row['Length']))
            )

        return road_segment

    def build_speed_reading(self, row, road):
        """
        Creates a SpeedReading object to be saved later in chunks.
        """
        return SpeedReading(
            road_segment=road,
            speed=float(row['Speed']),
            created_at=timezone.now()
        )

    def save_speed_readings(self, readings):
        """
        Bulk saves the speed readings to the database.
        """
        SpeedReading.objects.bulk_create(readings)
