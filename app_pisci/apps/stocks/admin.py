from django.contrib import admin
from .models import LotDePoisson

@admin.register(LotDePoisson)
class LotDePoissonAdmin(admin.ModelAdmin):
    list_display = ('code_lot', 'espece', 'site_prod', 'bassin', 'date_arrivee', 'quantite', 'statut')
    list_filter = ('site_prod', 'espece', 'statut')
    search_fields = ('code_lot', 'espece__nom_commun')
    ordering = ('-date_arrivee',)
    readonly_fields = ('poids_moyen', 'date_creation', 'date_modification')
