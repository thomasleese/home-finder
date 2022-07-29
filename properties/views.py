from django.views.generic import DetailView, ListView

from .models import Place, Property


class PlaceListView(ListView):
    queryset = Place.objects.order_by("name")
    paginate_by = 25


class PlaceDetailView(DetailView):
    model = Place


class PropertyListView(ListView):
    queryset = Property.objects.order_by("address")
    paginate_by = 25


class PropertyDetailView(DetailView):
    model = Property
