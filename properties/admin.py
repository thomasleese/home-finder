from django.contrib import admin

from .models import Place, Property, PropertyPlace


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "kind")
    list_filter = ("kind",)
    search_fields = ("name",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "price_sale",
        "price_rent_per_week",
        "price_rent_per_month",
        "number_of_bedrooms",
    )
    search_fields = ("address",)


@admin.register(PropertyPlace)
class PropertyPlaceAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "place",
        "driving_distance",
        "driving_duration",
        "cycling_distance",
        "cycling_duration",
        "walking_distance",
        "walking_duration",
        "transit_distance",
        "transit_duration",
    )
