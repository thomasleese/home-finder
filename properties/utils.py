from django.conf import settings

import googlemaps

from .models import PropertyPlace


def create_property_places(self, property, places):
    origins = [f"place_id:{property.google_place_id}"]
    destinations = [f"place_id:{place.google_id}" for place in places]

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    driving_results = gmaps.distance_matrix(origins, destinations, mode="driving")
    cycling_results = gmaps.distance_matrix(origins, destinations, mode="bicycling")
    walking_results = gmaps.distance_matrix(origins, destinations, mode="walking")
    transit_results = gmaps.distance_matrix(origins, destinations, mode="transit")

    for i, place in enumerate(places):
        property_place = PropertyPlace(property=property, place=place)

        try:
            driving_results = driving_results["rows"][0]["elements"][i]
            property_place.driving_distance = driving_results["distance"]["value"]
            property_place.driving_duration = driving_results["duration"]["value"]
        except KeyError:
            pass

        try:
            cycling_results = cycling_results["rows"][0]["elements"][i]
            property_place.cycling_distance = cycling_results["distance"]["value"]
            property_place.cycling_duration = cycling_results["duration"]["value"]
        except KeyError:
            pass

        try:
            walking_results = walking_results["rows"][0]["elements"][i]
            property_place.walking_distance = walking_results["distance"]["value"]
            property_place.walking_duration = walking_results["duration"]["value"]
        except KeyError:
            pass

        try:
            transit_results = transit_results["rows"][0]["elements"][i]
            property_place.transit_distance = transit_results["distance"]["value"]
            property_place.transit_duration = transit_results["duration"]["value"]
        except KeyError:
            pass

        property_place.save()
