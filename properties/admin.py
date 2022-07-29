from django.contrib import admin

from .models import Amenity, Property


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
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
