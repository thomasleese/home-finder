from django.urls import path

from .views import SearchDetailView, SearchPerformView


app_name = "searches"

urlpatterns = [
    path("<int:pk>", SearchDetailView.as_view(), name="search-detail"),
    path("<int:pk>/perform", SearchPerformView.as_view(), name="search-perform"),
]
