from django.urls import path
from .views import (
    SiteListView, SiteCreateView, SiteDeleteView, SiteUpdateView,
    BassinCreateView, BassinDeleteView, BassinListView, BassinUpdateView, BassinsAPIView, SiteListJsonView, BassinListJsonView, CarteBassinsView
)

app_name = "sites"
urlpatterns = [
    #Sites
    path("", SiteListView.as_view(), name="site-list"),
    path("list-json/", SiteListJsonView.as_view(), name="site-list-json"),  # <-- Nouvelle URL
    path("create/", SiteCreateView.as_view(), name="site-create"),
    path("<uuid:pk>/update/", SiteUpdateView.as_view(), name="site-update"),
    path("<uuid:pk>/delete/", SiteDeleteView.as_view(), name="site-delete"),
    # Bassins
    path("<uuid:site_id>/bassins/", BassinListView.as_view(), name="bassin-list"),
    path("<uuid:site_id>/bassins/list-json/", BassinListJsonView.as_view(), name="bassin-list-json"),
    path("<uuid:site_id>/bassins/create/", BassinCreateView.as_view(), name="bassin-create"),
    path("<uuid:site_id>/bassins/<uuid:pk>/update/", BassinUpdateView.as_view(), name="bassin-update"),
    path("<uuid:site_id>/bassins/<uuid:pk>/delete/", BassinDeleteView.as_view(), name="bassin-delete"),

    path('bassins/carte/', CarteBassinsView.as_view(), name='bassins_carte'),
]
