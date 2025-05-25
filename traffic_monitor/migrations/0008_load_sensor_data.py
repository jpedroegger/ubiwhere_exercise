import csv
import os
from django.db import migrations
from pathlib import Path


def load_sensor_data(apps, schema_editor):
    Sensor = apps.get_model("traffic_monitor", "Sensor")
    BASE_DIR = Path(__file__).resolve().parents[2]
    csv_file_path = BASE_DIR / "sensors.csv"

    if not os.path.isfile(csv_file_path):
        print(f"sensors.csv not found at {csv_file_path}. Skipping sensor data import.")
        return

    try:
        with open(csv_file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Sensor.objects.create(
                    name=row["name"],
                    uuid=row["uuid"],
                )
        print(" Sensor data loaded successfully.")
    except Exception as e:
        print(f"Error loading sensor data: {e}. Skipping import.")


def reverse_migration(apps, schema_editor):
    Sensor = apps.get_model("sensor", "Sensor")

    Sensor.objects.all().delete()


class Migration(migrations.Migration):
    """
    Load CSV sensor file into the database in migrations,
    so the sensor will be available after build.
    """

    dependencies = [
        ("traffic_monitor", "0007_autocreate_traffic_classifications"),
    ]

    operations = [
        migrations.RunPython(load_sensor_data, reverse_migration),
    ]
