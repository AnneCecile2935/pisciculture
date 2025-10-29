from django.urls import path
from . import views  # Import depuis le dossier courant (activité_quotidien)
from apps.activite_quotidien.views import NourrissageCreateView, NourrissageDeleteView, RelevesListJsonView, NourrissageListJsonView, NourrissageDetailView, ChoixSiteEnregistrementRepasView, NourrissageUpdateView, NourrissageListView, NourrissageParSiteView, ListRelevesView, CreateReleveView, DeleteReleveView, UpdateReleveView

app_name = 'activite_quotidien'  # Namespace pour éviter les conflits
urlpatterns = [
    # Nourrissage
    path('ajouter/', NourrissageCreateView.as_view(), name='nourrissage-create'),
    path('', NourrissageListView.as_view(), name='nourrissage-list'),
    path('<uuid:pk>/', NourrissageDetailView.as_view(), name='nourrissage-detail'),
    path('<uuid:pk>/update/', NourrissageUpdateView.as_view(), name='nourrissage-update'),
    path('<uuid:pk>/delete/', NourrissageDeleteView.as_view(), name='nourrissage-delete'),
    path('nourrissages/list/json/', NourrissageListJsonView.as_view(), name='nourrissage-list-json'),
    path('enregistrer-repas/<uuid:site_id>/', NourrissageParSiteView.as_view(), name='enregistrer-repas-par-site'),
    path('choisir-site/', ChoixSiteEnregistrementRepasView.as_view(), name='choisir-site-enregistrement-repas'),
    # Relevés
    path('releves/', ListRelevesView.as_view(), name='releve-list'),
    path('releves/ajouter/', CreateReleveView.as_view(), name='releve-create'),
    path('releves/<uuid:pk>/update/', UpdateReleveView.as_view(), name='releve-update'),
    path('releves/<uuid:pk>/delete/', DeleteReleveView.as_view(), name='releve-delete'),
    path('releves/list/json/', RelevesListJsonView.as_view(), name='releve-list-json'),
]
