# Generated by Django 4.0.6 on 2022-07-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0004_rename_amenity_place_alter_place_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="kind",
            field=models.CharField(
                choices=[
                    ("bus_station", "Bus station"),
                    ("gym", "Gym"),
                    ("light_rail_station", "Light rail station"),
                    ("park", "Park"),
                    ("restaurant", "Restaurant"),
                    ("school", "School"),
                    ("subway_station", "Subway station"),
                    ("train_station", "Train station"),
                ],
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name="PropertyPlace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "driving_distance",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "driving_duration",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "cycling_distance",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "cycling_duration",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "walking_distance",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "walking_duration",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "transit_distance",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "transit_duration",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    "place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="properties.place",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="properties.property",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "properties",
            },
        ),
        migrations.AddConstraint(
            model_name="propertyplace",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("driving_distance__isnull", False),
                        ("driving_duration__isnull", False),
                    ),
                    models.Q(
                        ("driving_distance__isnull", True),
                        ("driving_duration__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="valid_driving",
            ),
        ),
        migrations.AddConstraint(
            model_name="propertyplace",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("cycling_distance__isnull", False),
                        ("cycling_duration__isnull", False),
                    ),
                    models.Q(
                        ("cycling_distance__isnull", True),
                        ("cycling_duration__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="valid_cycling",
            ),
        ),
        migrations.AddConstraint(
            model_name="propertyplace",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("walking_distance__isnull", False),
                        ("walking_duration__isnull", False),
                    ),
                    models.Q(
                        ("walking_distance__isnull", True),
                        ("walking_duration__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="valid_walking",
            ),
        ),
        migrations.AddConstraint(
            model_name="propertyplace",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("transit_distance__isnull", False),
                        ("transit_duration__isnull", False),
                    ),
                    models.Q(
                        ("transit_distance__isnull", True),
                        ("transit_duration__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="valid_transit",
            ),
        ),
    ]
