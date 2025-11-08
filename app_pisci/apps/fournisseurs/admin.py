from django.contrib import admin
from .models import Fournisseur

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les fournisseurs.

    Cette classe personnalise l'affichage et la gestion des fournisseurs dans
    l'interface d'administration de Django, avec les fonctionnalités suivantes :
    - Liste des fournisseurs avec leur nom, ville, type et statut d'activité
    - Filtres par type de fournisseur et statut d'activité
    - Recherche par nom, ville ou contact

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des fournisseurs.
            Inclut :
            - nom (str): Nom du fournisseur (ex: "Aquaculture Bretonne")
            - ville (str): Ville de localisation (ex: "Rennes")
            - get_type_fournisseur_display (method): Type de fournisseur (affiché sous forme lisible)
            - est_actif (bool): Statut d'activité (True=actif, False=inactif)
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            Permet de filtrer par :
            - type_fournisseur : Type de fournisseur (aliment, équipement, etc.)
            - est_actif : Statut d'activité
        search_fields (tuple): Champs utilisables pour la recherche textuelle.
            Permet de rechercher par nom, ville ou contact du fournisseur.
    """
    list_display = ('nom', 'ville', 'get_type_fournisseur_display', 'est_actif')
    list_filter = ('type_fournisseur', 'est_actif')
    search_fields = ('nom', 'ville', 'contact')
    ordering = ('nom',) 
