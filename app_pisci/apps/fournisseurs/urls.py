from django.urls import path
from .views import FournisseurCreateView, FournisseurDeleteView, FournisseurListView, FournisseurUpdateView

app_name = 'fournisseurs'

urlpatterns = [
    path('', FournisseurListView.as_view(), name='fournisseur-list'),
    path('create/', FournisseurCreateView.as_view(), name='fournisseur-create'),
    path("<int:pk>/update/", FournisseurUpdateView.as_view(), name="fournisseur-update"),
    path("<int:pk>/delete/", FournisseurDeleteView.as_view(), name="fournisseur-delete"),
]

