from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .models import Search


class SearchDetailView(DetailView):
    model = Search


class SearchPerformView(UpdateView):
    model = Search
    fields = []
