from django.contrib import admin
from .models import LotDePoisson

@admin.register(LotDePoisson)
class LotDePoissonAdmin(admin.ModelAdmin):
    list_display = (
        'site_prod', 'bassin', 'espece',
        'fournisseur',
        'date_arrivee', 'quantite', 'statut', 'code_lot', 'poids'
    )
    list_filter = ('site_prod', 'fournisseur')
    search_fields = ('site_prod', 'bassin', 'fournisseur', 'statut', 'code_lot')

