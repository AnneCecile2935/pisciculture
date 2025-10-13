from django.urls import path
from .views import (
    SiteListView, SiteCreateView, SiteDeleteView, SiteUpdateView,
    BassinCreateView, BassinDeleteView, BassinListView, BassinUpdateView
)

app_name = "sites"
urlpatterns = [
    #Sites
    path("", SiteListView.as_view(), name="site-list"),
    path("create/", SiteCreateView.as_view(), name="site-create" ),
    path("<uuid:pk>/update/", SiteUpdateView.as_view(), name="site-update"),
    path("<uuid:pk>/delete/", SiteDeleteView.as_view(), name="site-delete"),

    #Bassins
    path("<uuid:site_id>/bassins/", BassinListView.as_view(), name="bassin-list"),
    path("bassins/create/", BassinCreateView.as_view(), name="bassin-create"),
    path("bassins/<uuid:pk>/update/", BassinUpdateView.as_view(), name="bassin-update"),
    path("bassins/<uuid:pk>/delete", BassinDeleteView.as_view(), name="bassin-delete"),
]
