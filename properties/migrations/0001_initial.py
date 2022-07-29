# Generated by Django 4.0.6 on 2022-07-29 06:51

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Property",
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
                ("zoopla_id", models.PositiveBigIntegerField()),
                ("address", models.TextField()),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("url", models.URLField()),
                ("price_sale", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "price_rent_per_week",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "price_rent_per_month",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "photos",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), size=None
                    ),
                ),
                ("number_of_bedrooms", models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="property",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("price_rent_per_month__isnull", True),
                        ("price_rent_per_week__isnull", True),
                        ("price_sale__isnull", False),
                    ),
                    models.Q(
                        ("price_rent_per_month__isnull", False),
                        ("price_rent_per_week__isnull", False),
                        ("price_sale__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="valid_price",
            ),
        ),
    ]
