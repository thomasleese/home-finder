from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Property(models.Model):
    zoopla_id = models.PositiveBigIntegerField()

    address = models.TextField()
    location = models.PointField()

    url = models.URLField()

    price_sale = models.PositiveIntegerField(null=True, blank=True)
    price_rent_per_week = models.PositiveIntegerField(null=True, blank=True)
    price_rent_per_month = models.PositiveIntegerField(null=True, blank=True)

    photos = ArrayField(models.URLField())
    number_of_bedrooms = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    price_sale__isnull=False,
                    price_rent_per_week__isnull=True,
                    price_rent_per_month__isnull=True,
                )
                | models.Q(
                    price_sale__isnull=True,
                    price_rent_per_week__isnull=False,
                    price_rent_per_month__isnull=False,
                ),
                name="valid_price",
            ),
        ]
