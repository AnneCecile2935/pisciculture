from django.urls import path
from .views import LotListView, LotCreateView, LotUpdateView, LotDeleteView, LotListJsonView

app_name = "stocks"
urlpatterns = [
    path("", LotListView.as_view(), name="list"),
    path("list-json/", LotListJsonView.as_view(), name="list-json"),
    path("create/", LotCreateView.as_view(), name="create"),
    path("<uuid:pk>/update/", LotUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", LotDeleteView.as_view(), name="delete"),
]
