# Generated by Django 5.2.1 on 2025-05-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_monitor", "0002_trafficclassification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roadsegment",
            name="road_length",
            field=models.FloatField(),
        ),
    ]
