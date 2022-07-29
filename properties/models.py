from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Property(models.Model):
    zoopla_id = models.PositiveBigIntegerField()

    address = models.TextField()

    google_place_id = models.CharField(max_length=256, blank=True, default="")
    location = models.PointField()

    url = models.URLField()

    price_sale = models.PositiveIntegerField(null=True, blank=True)
    price_rent_per_week = models.PositiveIntegerField(null=True, blank=True)
    price_rent_per_month = models.PositiveIntegerField(null=True, blank=True)

    photos = ArrayField(models.URLField())
    number_of_bedrooms = models.PositiveSmallIntegerField()

    imported_amenities_at = models.DateTimeField(null=True, blank=True)

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

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("properties:property-detail", kwargs={"pk": self.pk})


class PlaceManager(models.Manager):
    def update_or_create_from_google(self, kind, result):
        google_id = result["place_id"]
        name = result["name"]
        location = Point(
            result["geometry"]["location"]["lng"], result["geometry"]["location"]["lat"]
        )

        return self.update_or_create(
            google_id=google_id,
            defaults={"name": name, "location": location, "kind": kind},
        )


class Place(models.Model):
    class Kind(models.TextChoices):
        BUS_STATION = "bus_station", _("Bus station")
        ESTABLISHMENT = "establishment", _("Establishment")
        GYM = "gym", _("Gym")
        LIGHT_RAIL_STATION = "light_rail_station", _("Light rail station")
        PARK = "park", _("Park")
        PREMISE = "premise", _("Premise")
        RESTAURANT = "restaurant", _("Restaurant")
        SCHOOL = "school", _("School")
        SUBWAY_STATION = "subway_station", _("Subway station")
        TRAIN_STATION = "train_station", _("Train station")

    google_id = models.CharField(max_length=128)

    name = models.TextField()
    location = models.PointField()
    kind = models.CharField(max_length=32, choices=Kind.choices)

    objects = PlaceManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("properties:place-detail", kwargs={"pk": self.pk})


class PropertyPlace(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property_places"
    )
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="property_places"
    )

    driving_distance = models.PositiveBigIntegerField(null=True, blank=True)
    driving_duration = models.PositiveBigIntegerField(null=True, blank=True)
    cycling_distance = models.PositiveBigIntegerField(null=True, blank=True)
    cycling_duration = models.PositiveBigIntegerField(null=True, blank=True)
    walking_distance = models.PositiveBigIntegerField(null=True, blank=True)
    walking_duration = models.PositiveBigIntegerField(null=True, blank=True)
    transit_distance = models.PositiveBigIntegerField(null=True, blank=True)
    transit_duration = models.PositiveBigIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property", "place"], name="property_place_unique"
            ),
            models.CheckConstraint(
                check=models.Q(
                    driving_distance__isnull=False,
                    driving_duration__isnull=False,
                )
                | models.Q(
                    driving_distance__isnull=True,
                    driving_duration__isnull=True,
                ),
                name="valid_driving",
            ),
            models.CheckConstraint(
                check=models.Q(
                    cycling_distance__isnull=False,
                    cycling_duration__isnull=False,
                )
                | models.Q(
                    cycling_distance__isnull=True,
                    cycling_duration__isnull=True,
                ),
                name="valid_cycling",
            ),
            models.CheckConstraint(
                check=models.Q(
                    walking_distance__isnull=False,
                    walking_duration__isnull=False,
                )
                | models.Q(
                    walking_distance__isnull=True,
                    walking_duration__isnull=True,
                ),
                name="valid_walking",
            ),
            models.CheckConstraint(
                check=models.Q(
                    transit_distance__isnull=False,
                    transit_duration__isnull=False,
                )
                | models.Q(
                    transit_distance__isnull=True,
                    transit_duration__isnull=True,
                ),
                name="valid_transit",
            ),
        ]
