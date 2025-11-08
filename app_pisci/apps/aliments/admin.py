from django.contrib import admin
from .models import Aliment

@admin.register(Aliment)
class AlimentAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les aliments.

    Cette classe personnalise l'affichage et le comportement des aliments
    dans l'interface d'administration de Django, avec :
    - Une liste claire des colonnes à afficher
    - Une barre de recherche fonctionnelle
    - Des filtres par fournisseur

    Attributes:
        list_display (tuple): Champs à afficher dans la liste des aliments.
            Comprend le code, le nom et le fournisseur de chaque aliment.
        search_fields (tuple): Champs utilisables pour la recherche.
            Permet de rechercher par code ou nom d'aliment.
        list_filter (tuple): Champs utilisables pour filtrer la liste.
            Permet de filtrer les aliments par fournisseur.
    """
    list_display = ("code_alim", "nom", "fournisseur", "description")
    search_fields = ("code_alim", "nom")
    list_filter = ("fournisseur",)
