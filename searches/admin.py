from django.contrib import admin

from .models import Search, TravelTimeRequirement


class TravelTimeRequirementInline(admin.StackedInline):
    model = TravelTimeRequirement
    raw_id_fields = ("place",)


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "max_price_sale",
        "max_price_rent_per_week",
        "max_price_rent_per_month",
    )
    inlines = (TravelTimeRequirementInline,)
