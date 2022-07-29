from django.urls import path

from .views import PlaceDetailView, PlaceListView, PropertyDetailView, PropertyListView


app_name = "properties"

urlpatterns = [
    path("", PropertyListView.as_view(), name="property-list"),
    path("<int:pk>", PropertyDetailView.as_view(), name="property-detail"),
    path("places", PlaceListView.as_view(), name="place-list"),
    path("places/<int:pk>", PlaceDetailView.as_view(), name="place-detail"),
]
