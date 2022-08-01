from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.core.management.base import BaseCommand
from django.utils import timezone
import googlemaps

from properties.models import Place, Property


class Command(BaseCommand):
    help = "Import all amenities from Google"

    place_kinds = [
        Place.Kind.BUS_STATION,
        Place.Kind.GYM,
        Place.Kind.LIGHT_RAIL_STATION,
        Place.Kind.PARK,
        Place.Kind.RESTAURANT,
        Place.Kind.SUBWAY_STATION,
        Place.Kind.TRAIN_STATION,
    ]

    def handle(self, *args, **options):
        properties = Property.objects.filter(imported_amenities_at__isnull=True)
        count = properties.count()

        for i, property in enumerate(properties):
            has_amenities = Place.objects.annotate(
                distance=Distance("location", property.location)
            ).filter(distance__lte=500).exists()

            if has_amenities:
                continue

            self.stdout.write(self.style.MIGRATE_HEADING(f"{property.address} ({i+1}/{count})"))

            for kind in self.place_kinds:
                try:
                    self.import_amenities(property, kind)
                except googlemaps.exceptions.ApiError:
                    break

            property.imported_amenities_at = timezone.now()
            property.save()

    def import_amenities(self, property, kind):
        self.stdout.write(f" - {kind}")

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        response = gmaps.places_nearby(
            location=property.location.coords, type=kind.value, rank_by="distance"
        )

        for result in response["results"]:
            Place.objects.update_or_create_from_google(kind, result)
