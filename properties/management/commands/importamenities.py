from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
import googlemaps

from properties.models import Amenity, Property


class Command(BaseCommand):
    help = "Import all amenities from Google"

    def handle(self, *args, **options):
        for property in Property.objects.all():
            for kind in Amenity.Kind:
                self.import_amenities(property, kind)

    def import_amenities(self, property, kind):
        self.stdout.write(f"Importing '{kind}' for '{property.address}'")

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        response = gmaps.places_nearby(
            location=property.location.coords, type=kind.value, rank_by="distance"
        )

        for place in response["results"]:
            self.import_place(kind, place)

    def import_place(self, kind, place):
        self.stdout.write(f"Importing '{place['name']}'")

        google_id = place["place_id"]
        name = place["name"]
        location = Point(
            place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]
        )

        Amenity.objects.update_or_create(
            google_id=google_id,
            defaults={"name": name, "location": location, "kind": kind},
        )
