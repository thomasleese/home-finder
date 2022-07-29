from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
import googlemaps


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

    def fetch_location(self):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        geocode_results = gmaps.geocode(self.address)
        try:
            location = geocode_results[0]['geometry']['location']
        except IndexError:
            self.location = None
        else:
            self.location = Point(location['lat'], location['lng'])
