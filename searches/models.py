from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from properties.models import Place, Property


class Search(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="searches"
    )

    max_price_sale = models.PositiveIntegerField(null=True, blank=True)
    max_price_rent_per_week = models.PositiveIntegerField(null=True, blank=True)
    max_price_rent_per_month = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "searches"

    def get_absolute_url(self):
        return reverse("searches:search-detail", kwargs={"pk": self.pk})


class TravelTimeRequirement(models.Model):
    search = models.ForeignKey(
        Search, on_delete=models.CASCADE, related_name="travel_time_requirements"
    )

    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name=None, null=True, blank=True
    )
    place_kind = models.CharField(max_length=32, choices=Place.Kind.choices, blank=True)

    class Mode(models.TextChoices):
        DRIVING = "driving", _("Driving")
        CYCLING = "cycling", _("Cycling")
        WALKING = "walking", _("Walking")
        TRANSIT = "transit", _("Public transport")

    mode = models.CharField(max_length=8, choices=Mode.choices)

    max_distance = models.PositiveBigIntegerField(null=True, blank=True)
    max_duration = models.PositiveBigIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    place__isnull=False,
                    place_kind="",
                )
                | (models.Q(place__isnull=True) & ~models.Q(place_kind="")),
                name="valid_place_or_place_kind",
            ),
        ]


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE, related_name="results")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name=None)
