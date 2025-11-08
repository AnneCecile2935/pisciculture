from django.contrib import admin
from .models import ReleveTempOxy, Nourrissage

# Enregistrement des modèles dans l'admin Django
admin.site.register(Nourrissage)
admin.site.register(ReleveTempOxy)

class NourrissageAdmin(admin.ModelAdmin):
    """
    Configuration personnalisée pour l'interface d'administration des nourrissages.

    Cette classe permet d'afficher et de gérer les enregistrements de nourrissage
    dans l'interface d'administration de Django avec des colonnes personnalisées.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des nourrissages.
            Inclut des champs du modèle et des méthodes personnalisées.
    """
    list_display = (
        'code_lot', 'bassin',
        'date_repas', 'qte', 'aliment',
        'site_prod', 'notes'
    )
    list_filter = ('date_repas', 'aliment', 'site_prod')  # Filtres latéraux
    search_fields = ('lot__code_lot', 'bassin__nom')      # Champ de recherche
    date_hierarchy = 'date_repas'                

    def code_lot(self, obj):
        """
        Récupère le code du lot de poissons associé au nourrissage.

        Cette méthode est utilisée pour afficher le code du lot dans la liste
        des nourrissages, même si ce champ n'existe pas directement dans le modèle Nourrissage.

        Args:
            obj (Nourrissage): Instance du modèle Nourrissage en cours d'affichage.

        Returns:
            str: Le code du lot de poissons associé (via la relation avec LotDePoisson).
        """
        return obj.code_lot
    code_lot.short_description = "Code lot"

