from django.urls import path
from . import views  # Import depuis le dossier courant (activité_quotidien)

app_name = 'activité_quotidien'  # Namespace pour éviter les conflits
urlpatterns = [
    path('', views.index, name='index'),
    path('releves/', views.liste_releves, name='liste_releves'),
    path('releves/ajouter/', views.ajouter_releve, name='ajouter_releve'),
    path('releves/manquants/', views.releves_manquants, name='releves_manquants'),
]
