from django.contrib import admin
from .models import Site, Bassin

# Enregistrement du modèle Site avec sa configuration admin personnalisée

admin.site.register(Site)
class SiteAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les sites de production.

    Cette classe personnalise l'affichage et la gestion des sites dans l'interface
    d'administration de Django, avec les fonctionnalités suivantes :
    - Liste des sites avec leur nom, statut d'activité et date de création
    - Filtre par statut d'activité
    - Recherche par nom de site
    - Tri par défaut du plus récent au plus ancien

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des sites.
            Inclut :
            - nom (str): Nom du site (ex: "Site de Plougastel")
            - est_actif (bool): Statut d'activité (True=actif, False=inactif)
            - created_at (datetime): Date de création du site
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            Permet de filtrer par statut d'activité.
        search_fields (tuple): Champs utilisables pour la recherche textuelle.
            Permet de rechercher un site par son nom.
        ordering (tuple): Ordre de tri par défaut.
            Affiche les sites du plus récent au plus ancien.
    """
    list_display = ('nom', 'est_actif', 'created_at')
    list_filter = ('est_actif',)
    search_fields = ('nom',)
    ordering = ('-created_at',)

# Enregistrement du modèle Bassin avec sa configuration admin personnalisée
admin.site.register(Bassin)

class BassinAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les bassins.

    Cette classe personnalise l'affichage et la gestion des bassins dans l'interface
    d'administration de Django, avec les fonctionnalités suivantes :
    - Liste des bassins avec leur nom, site parent, volume, type et statut
    - Filtres par site, type de bassin et statut d'activité
    - Recherche par nom ou type de bassin
    - Tri par défaut du plus récent au plus ancien

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des bassins.
            Inclut :
            - nom (str): Nom du bassin (ex: "Bassin A1")
            - site (ForeignKey): Site de production auquel appartient le bassin
            - volume (float): Volume en m³
            - type (str): Type de bassin (ex: "Écloserie", "Grossissement")
            - est_actif (bool): Statut d'activité
            - created_at (datetime): Date de création
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            Permet de filtrer par site, type de bassin ou statut d'activité.
        search_fields (tuple): Champs utilisables pour la recherche textuelle.
            Permet de rechercher un bassin par son nom ou son type.
        ordering (tuple): Ordre de tri par défaut.
            Affiche les bassins du plus récent au plus ancien.
    """
    list_display = ('nom', 'site', 'volume', 'type', 'est_actif', 'created_at')
    list_filter = ('site', 'type', 'est_actif')
    search_fields = ('nom', 'type')
    ordering = ('-created_at',)
