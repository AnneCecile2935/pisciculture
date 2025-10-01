from django.urls import path
from .views import FournisseurListView, FournisseurCreateView, FournisseurUpdateView

urlpatterns = [
    path('', FournisseurListView.as_view(), name='fournisseur_list'),
    path('ajouter/', FournisseurCreateView.as_view(), name='fournisseur_add'),
    path('<int:pk>/modifier/', FournisseurUpdateView.as_view(), name='fournisseur_edit'),
]
