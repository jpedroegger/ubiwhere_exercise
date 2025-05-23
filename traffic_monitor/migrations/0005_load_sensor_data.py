import csv
import os
from django.db import migrations
from django.conf import settings


def load_sensor_data(apps, schema_editor):
    Sensor = apps.get_model('traffic_monitor', 'Sensor')
    
    # app_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join('sensors.csv')

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Sensor.objects.create(
                id=row['id'],
                name=row['name'],
                uuid=row['uuid'],      
            )

def reverse_migration(apps, schema_editor):
    Sensor = apps.get_model('sensor', 'Sensor')

    Sensor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('traffic_monitor', '0004_car_sensor_trafficrecord'),
    ]

    operations = [
        migrations.RunPython(load_sensor_data, reverse_migration),
    ]
