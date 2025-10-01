from django.contrib import admin
from .models import Aliment

@admin.register(Aliment)
class AlimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'fournisseur', 'categorie', 'description')
    list_filter = ('fournisseur',)
    search_fields = ('categorie', 'fournisseur__nom')
