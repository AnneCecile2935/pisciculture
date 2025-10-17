from django.urls import path
from . import views  # Import depuis le dossier courant (activité_quotidien)
from apps.activite_quotidien.views import NourrissageCreateView, NourrissageDeleteView,NourrissageListJsonView, NourrissageDetailView, NourrissageUpdateView, NourrissageListView

app_name = 'activite_quotidien'  # Namespace pour éviter les conflits
urlpatterns = [
    path('ajouter/', NourrissageCreateView.as_view(), name='nourrissage-create'),
    path('', NourrissageListView.as_view(), name='nourrissage-list'),
    path('<uuid:pk>/', NourrissageDetailView.as_view(), name='nourrissage-detail'),
    path('<uuid:pk>/modifier/', NourrissageUpdateView.as_view(), name='nourrissage-update'),
    path('<uuid:pk>/supprimer/', NourrissageDeleteView.as_view(), name='nourrissage-delete'),
    path('nourrissages/list/json/', NourrissageListJsonView.as_view(), name='nourrissage-list-json'),
    path('', views.index, name='index'),
    path('releves/', views.liste_releves, name='liste_releves'),
    path('releves/ajouter/', views.ajouter_releve, name='ajouter_releve'),
    path('releves/manquants/', views.releves_manquants, name='releves_manquants'),
]
