from django.contrib import admin
from .models import LotDePoisson


class LotDePoissonAdmin(admin.ModelAdmin):
    list_display = ('code_lot', 'espece', 'site_prod', 'get_bassins', 'date_arrivee', 'quantite', 'statut')
    list_filter = ('site_prod', 'espece', 'statut')
    search_fields = ('code_lot', 'espece__nom_commun')
    ordering = ('-date_arrivee',)
    readonly_fields = ('poids_moyen', 'date_creation', 'date_modification')

    def get_bassins(self, obj):
        return ", ".join([bassin.nom for bassin in obj.bassins.all()])
    get_bassins.short_description = "Bassins"

admin.site.register(LotDePoisson, LotDePoissonAdmin)
