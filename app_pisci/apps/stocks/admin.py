from django.contrib import admin
from .models import LotDePoisson


class LotDePoissonAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les lots de poissons.

    Cette classe personnalise l'affichage et la gestion des lots de poissons dans
    l'interface d'administration de Django, avec les fonctionnalités suivantes :
    - Liste des lots avec leurs informations clés (code, espèce, site, bassins, etc.)
    - Filtres par site de production, espèce et statut
    - Recherche par code de lot ou nom commun de l'espèce
    - Tri par défaut du plus récent au plus ancien
    - Champs en lecture seule pour les données calculées ou systématiques

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des lots.
            Inclut :
            - code_lot (str): Code unique du lot (ex: "TRU-2023-001")
            - espece (ForeignKey): Espèce de poisson (affichée par son nom commun)
            - site_prod (ForeignKey): Site de production
            - get_bassins (method): Liste des bassins associés au lot
            - date_arrivee (date): Date d'arrivée du lot sur le site
            - quantite (int): Quantité initiale de poissons
            - quantite_actuelle (int): Quantité actuelle de poissons (après mortalités)
            - poids_moyen (float): Poids moyen des poissons (en kg, calculé automatiquement)
            - statut (str): Statut actuel du lot (ex: "En croissance", "Vendu")
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            Permet de filtrer par site, espèce ou statut.
        search_fields (tuple): Champs utilisables pour la recherche textuelle.
            Permet de rechercher par code de lot ou nom commun de l'espèce.
        ordering (tuple): Ordre de tri par défaut.
            Affiche les lots du plus récent au plus ancien.
        readonly_fields (tuple): Champs en lecture seule.
            Inclut les champs calculés ou gérés automatiquement.
    """
    list_display = ('code_lot', 'espece', 'site_prod', 'get_bassins', 'date_arrivee', 'quantite', 'quantite_actuelle', 'poids_moyen', 'statut')
    list_filter = ('site_prod', 'espece', 'statut')
    search_fields = ('code_lot', 'espece__nom_commun')
    ordering = ('-date_arrivee',)
    readonly_fields = ('poids_moyen', 'date_creation', 'date_modification')

    def get_bassins(self, obj):
        """
        Récupère et formate la liste des bassins associés à ce lot.

        Cette méthode permet d'afficher tous les bassins où ce lot a été
        ou est actuellement présent, séparés par des virgules.

        Args:
            obj (LotDePoisson): Instance du modèle LotDePoisson

        Returns:
            str: Liste des noms de bassins séparés par des virgules.
                 Retourne une chaîne vide si aucun bassin n'est associé.
        """
        return ", ".join([bassin.nom for bassin in obj.bassins.all()])

    get_bassins.short_description = "Bassins"
    
# Enregistrement du modèle avec sa configuration admin personnalisée
admin.site.register(LotDePoisson, LotDePoissonAdmin)
