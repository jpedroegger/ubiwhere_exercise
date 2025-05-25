from django.db import migrations


def create_traffic_classifications(apps, schema_editor):
    TrafficClassification = apps.get_model("traffic_monitor", "TrafficClassification")

    classifications = [
        {"name": "HIGH", "min_speed": 0, "max_speed": 20.99},
        {"name": "MEDIUM", "min_speed": 21.0, "max_speed": 50.99},
        {"name": "LOW", "min_speed": 51.0, "max_speed": None},
    ]

    for cls in classifications:
        TrafficClassification.objects.update_or_create(
            name=cls["name"],
            defaults={
                "min_speed": cls["min_speed"],
                "max_speed": cls["max_speed"],
            },
        )


def remove_traffic_classifications(apps, schema_editor):
    TrafficClassification = apps.get_model("traffic_monitor", "TrafficClassification")
    TrafficClassification.objects.filter(name__in=["LOW", "MEDIUM", "HIGH"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_monitor", "0006_alter_trafficrecord_timestamp"),
    ]

    operations = [
        migrations.RunPython(
            create_traffic_classifications, remove_traffic_classifications
        ),
    ]
