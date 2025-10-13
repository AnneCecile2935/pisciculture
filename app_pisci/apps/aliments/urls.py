from django.urls import path
from .views import AlimentCreateView, AlimentDeleteView, AlimentListView, AlimentUpdateView

app_name = "aliments"

urlpatterns = [
    path("", AlimentListView.as_view(), name="list"),
    path("create/", AlimentCreateView.as_view(), name="create"),
    path("<uuid:pk>/update/", AlimentUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", AlimentDeleteView.as_view(), name="delete"),
]
