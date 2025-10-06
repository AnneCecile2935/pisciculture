from django.urls import path
from .views import AlimentCreateView, AlimentDeleteView, AlimentListView, AlimentUpdateView

app_name = "aliments"

urlpatterns = [
    path("", AlimentListView.as_view(), name="list"),
    path("ajouter/", AlimentCreateView.as_view(), name="create"),
    path("<int:pk>/editer/", AlimentUpdateView.as_view(), name="update"),
    path("<int:pk>/supprimer/", AlimentDeleteView.as_view(), name="delete"),
]
