from django.contrib.gis.db.models.functions import Distance
from django.core.management.base import BaseCommand

from properties.models import Place, Property, PropertyPlace
from properties.utils import create_property_places


class Command(BaseCommand):
    help = "Import all amenities from Google"

    def handle(self, *args, **options):
        for property in Property.objects.exclude(google_place_id=""):
            self.stdout.write(self.style.MIGRATE_HEADING(property.address))

            closest_places = Place.objects.annotate(
                distance=Distance("location", property.location)
            ).order_by("distance")[:100]

            for place in closest_places:
                self.stdout.write(f" - {place.name} ({place.kind})")

            create_property_places([property], closest_places)
