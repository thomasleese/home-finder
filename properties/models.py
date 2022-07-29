from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
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
        verbose_name_plural = "properties"
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
            location = geocode_results[0]["geometry"]["location"]
        except IndexError:
            self.location = None
        else:
            self.location = Point(location["lng"], location["lat"])


class Amenity(models.Model):
    class Kind(models.TextChoices):
        BUS_STATION = "bus_station", _("Bus station")
        GYM = "gym", _("Gym")
        LIGHT_RAIL_STATION = "light_rail_station", _("Light rail station")
        PARK = "park", _("Park")
        RESTAURANT = "restaurant", _("Restaurant")
        SUBWAY_STATION = "subway_station", _("Subway station")
        TRAIN_STATION = "train_station", _("Train station")

    google_id = models.CharField(max_length=128)

    name = models.TextField()
    location = models.PointField()
    kind = models.CharField(max_length=32, choices=Kind.choices)

    class Meta:
        verbose_name_plural = "amenities"

    def __str__(self):
        return self.name
