from django.contrib import admin
from .models import Espece

@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les espèces de poissons.

    Cette classe personnalise l'affichage et la gestion des espèces dans l'interface
    d'administration de Django, avec les fonctionnalités suivantes :
    - Liste des espèces avec leur nom commun, nom scientifique et statut d'activité
    - Filtre par statut d'activité (actif/inactif)
    - Recherche par nom commun ou nom scientifique

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des espèces.
            Inclut :
            - nom_commun (str): Nom usuel de l'espèce (ex: "Truite arc-en-ciel")
            - nom_scientifique (str): Nom scientifique (ex: "Oncorhynchus mykiss")
            - est_actif (bool): Statut de l'espèce (active ou inactive)
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            Permet de filtrer les espèces par leur statut (actif/inactif).
        search_fields (tuple): Champs utilisables pour la recherche textuelle.
            Permet de rechercher une espèce par son nom commun ou scientifique.
    """
    list_display = ('nom_commun', 'nom_scientifique', 'est_actif')
    list_filter = ('est_actif',)
    search_fields = ('nom_commun', 'nom_scientifique')
    ordering = ('nom_commun',)
