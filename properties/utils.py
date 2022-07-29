from django.conf import settings

import googlemaps

from .models import PropertyPlace


def create_property_places(properties, places):
    properties_set = set(properties)
    places_set = set(places)

    properties = [
        property
        for property in properties_set
        if not set(p.id for p in places_set)
        <= set(
            PropertyPlace.objects.filter(property=property).values_list(
                "place", flat=True
            )
        )
    ]

    places = [
        place
        for place in places_set
        if not set(p.id for p in properties_set)
        <= set(
            PropertyPlace.objects.filter(place=place).values_list("property", flat=True)
        )
    ]

    for i in range(0, len(properties), 25):
        for j in range(0, len(places), 25):
            _create_property_places(properties[i : i + 25], places[j : j + 25])


def _create_property_places(properties, places):
    origins = [f"place_id:{property.google_place_id}" for property in properties]
    destinations = [f"place_id:{place.google_id}" for place in places]

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    driving_results = gmaps.distance_matrix(origins, destinations, mode="driving")
    cycling_results = gmaps.distance_matrix(origins, destinations, mode="bicycling")
    walking_results = gmaps.distance_matrix(origins, destinations, mode="walking")
    transit_results = gmaps.distance_matrix(origins, destinations, mode="transit")

    for row, property in enumerate(properties):
        for el, place in enumerate(places):
            try:
                property_place = PropertyPlace.objects.get(
                    property=property, place=place
                )
            except PropertyPlace.DoesNotExist:
                property_place = PropertyPlace(property=property, place=place)

            try:
                driving_results_row = driving_results["rows"][row]["elements"][el]
                property_place.driving_distance = driving_results_row["distance"][
                    "value"
                ]
                property_place.driving_duration = driving_results_row["duration"][
                    "value"
                ]
            except (IndexError, KeyError):
                pass

            try:
                cycling_results_row = cycling_results["rows"][row]["elements"][el]
                property_place.cycling_distance = cycling_results_row["distance"][
                    "value"
                ]
                property_place.cycling_duration = cycling_results_row["duration"][
                    "value"
                ]
            except (IndexError, KeyError):
                pass

            try:
                walking_results_row = walking_results["rows"][row]["elements"][el]
                property_place.walking_distance = walking_results_row["distance"][
                    "value"
                ]
                property_place.walking_duration = walking_results_row["duration"][
                    "value"
                ]
            except (IndexError, KeyError):
                pass

            try:
                transit_results_row = transit_results["rows"][row]["elements"][el]
                property_place.transit_distance = transit_results_row["distance"][
                    "value"
                ]
                property_place.transit_duration = transit_results_row["duration"][
                    "value"
                ]
            except (IndexError, KeyError):
                pass

            property_place.save()
