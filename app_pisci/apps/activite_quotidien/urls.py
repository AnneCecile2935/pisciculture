from django.urls import path
from . import views  # Import depuis le dossier courant (activité_quotidien)
from apps.activite_quotidien.views import NourrissageCreateView, NourrissageDeleteView,NourrissageListJsonView, NourrissageDetailView, ChoixSiteEnregistrementRepasView, NourrissageUpdateView, NourrissageListView, NourrissageParSiteView

app_name = 'activite_quotidien'  # Namespace pour éviter les conflits
urlpatterns = [
    path('ajouter/', NourrissageCreateView.as_view(), name='nourrissage-create'),
    path('', NourrissageListView.as_view(), name='nourrissage-list'),
    path('<uuid:pk>/', NourrissageDetailView.as_view(), name='nourrissage-detail'),
    path('<uuid:pk>/update/', NourrissageUpdateView.as_view(), name='nourrissage-update'),
    path('<uuid:pk>/delete/', NourrissageDeleteView.as_view(), name='nourrissage-delete'),
    path('nourrissages/list/json/', NourrissageListJsonView.as_view(), name='nourrissage-list-json'),
    path('enregistrer-repas/<uuid:site_id>/', NourrissageParSiteView.as_view(), name='enregistrer-repas-par-site'),
    path('choisir-site/', ChoixSiteEnregistrementRepasView.as_view(), name='choisir-site-enregistrement-repas'),
    path('releves/', views.liste_releves, name='liste_releves'),
    path('releves/', views.liste_releves, name='liste_releves'),
    path('releves/ajouter/', views.ajouter_releve, name='ajouter_releve'),
    path('releves/manquants/', views.releves_manquants, name='releves_manquants'),
]
