from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from properties.models import Property, PropertyPlace
from properties.utils import create_property_places

from .models import Search


class SearchDetailView(DetailView):
    model = Search


class SearchPerformView(UpdateView):
    model = Search
    fields = []

    def form_valid(self, form):
        self.object.results.all().delete()

        properties = self.filter_properties_by_number_of_bedrooms(
            self.filter_properties_by_price(
                Property.objects.exclude(google_place_id="")
            )
        )

        self.create_properties_places(properties)

        properties = self.filter_properties_by_requirements(properties)

        for property in properties:
            self.object.results.create(property=property)

        return super().form_valid(form)

    def filter_properties_by_price(self, queryset):
        if max_price_sale := self.object.max_price_sale:
            queryset = queryset.filter(
                Q(price_sale__lte=max_price_sale) | Q(price_sale=None)
            )

        if max_price_rent_per_week := self.object.max_price_rent_per_week:
            queryset = queryset.filter(
                Q(price_rent_per_week__lte=max_price_rent_per_week)
                | Q(price_rent_per_week=None)
            )

        if max_price_rent_per_month := self.object.max_price_rent_per_month:
            queryset = queryset.filter(
                Q(price_rent_per_month__lte=max_price_rent_per_month)
                | Q(price_rent_per_month=None)
            )

        return queryset

    def filter_properties_by_number_of_bedrooms(self, queryset):
        if min_number_of_bedrooms := self.object.min_number_of_bedrooms:
            queryset = queryset.filter(number_of_bedrooms__gte=min_number_of_bedrooms)

        return queryset

    def create_properties_places(self, properties):
        places = [
            requirement.place
            for requirement in self.object.travel_time_requirements.exclude(
                place=None
            ).all()
        ]

        create_property_places(properties, places)

    def filter_properties_by_requirements(self, queryset):
        properties = []

        for property in queryset:
            for requirement in self.object.travel_time_requirements.all():
                if not self._test_requirement(requirement, property):
                    break
            else:
                properties.append(property)

        return properties

    def _test_requirement(self, requirement, property):
        if place := requirement.place:
            property_place = PropertyPlace.objects.get(property=property, place=place)

            if max_distance := requirement.max_distance:
                distance_field = f"{requirement.mode}_distance"
                if distance := getattr(property_place, distance_field):
                    if distance > max_distance:
                        return False

            if max_duration := requirement.max_duration:
                duration_field = f"{requirement.mode}_duration"
                if duration := getattr(property_place, duration_field):
                    if duration > max_duration:
                        return False

        return True
