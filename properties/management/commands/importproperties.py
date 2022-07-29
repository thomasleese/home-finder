import itertools

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
import googlemaps
from zoopla import Zoopla

from properties.models import Property


class Command(BaseCommand):
    help = "Import all properties from Zoopla"

    def handle(self, *args, **options):
        zoopla = Zoopla()

        regions = ["east-london", "west-london", "south-london", "north-london"]

        for region in regions:
            for page in itertools.count(1):
                self.stdout.write(
                    self.style.MIGRATE_HEADING(f"Rent {region} page #{page}")
                )
                properties = zoopla.get_to_rent_properties(region, page)
                if not properties:
                    break
                for property in properties:
                    self.import_property(property)

            for page in itertools.count(1):
                self.stdout.write(
                    self.style.MIGRATE_HEADING(f"Sale {region} page #{page}")
                )
                properties = zoopla.get_for_sale_properties(region, page)
                if not properties:
                    break
                for property in properties:
                    self.import_property(property)

    def import_property(self, zoopla_property):
        self.stdout.write(f" - {zoopla_property.address}")

        try:
            property = Property.objects.get(zoopla_id=zoopla_property.id)
        except Property.DoesNotExist:
            property = Property(zoopla_id=zoopla_property.id)

        property.address = zoopla_property.address
        property.url = zoopla_property.url

        if for_sale := zoopla_property.price.for_sale:
            property.price_sale = for_sale
        elif to_rent := zoopla_property.price.to_rent:
            property.price_rent_per_week = to_rent.per_week
            property.price_rent_per_month = to_rent.per_month
        else:
            self.stdout.write(self.style.WARNING("Skipped"))
            return

        property.photos = zoopla_property.photos
        property.number_of_bedrooms = zoopla_property.number_of_bedrooms

        if not property.location or not property.google_place_id:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_results = gmaps.geocode(property.address)
            try:
                google_place_id = geocode_results[0]["place_id"]
                location = geocode_results[0]["geometry"]["location"]
            except IndexError:
                self.stdout.write(self.style.WARNING("Skipped"))
                return
            else:
                property.google_place_id = google_place_id
                property.location = Point(location["lng"], location["lat"])

        property.save()
