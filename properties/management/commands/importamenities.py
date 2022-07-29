from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils import timezone
import googlemaps

from properties.models import Amenity, Property


class Command(BaseCommand):
    help = "Import all amenities from Google"

    def handle(self, *args, **options):
        for property in Property.objects.order_by(
            F("imported_amenities_at").desc(nulls_first=True)
        ):
            self.stdout.write(self.style.MIGRATE_HEADING(property.address))
            for kind in Amenity.Kind:
                self.import_amenities(property, kind)
            property.imported_amenities_at = timezone.now()
            property.save()

    def import_amenities(self, property, kind):
        self.stdout.write(f" - {kind}")

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        response = gmaps.places_nearby(
            location=property.location.coords, type=kind.value, rank_by="distance"
        )

        for place in response["results"]:
            self.import_place(kind, place)

    def import_place(self, kind, place):
        google_id = place["place_id"]
        name = place["name"]
        location = Point(
            place["geometry"]["location"]["lng"], place["geometry"]["location"]["lat"]
        )

        Amenity.objects.update_or_create(
            google_id=google_id,
            defaults={"name": name, "location": location, "kind": kind},
        )
