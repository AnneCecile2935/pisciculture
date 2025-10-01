from django.contrib import admin
from .models import Fournisseurs

@admin.register(Fournisseurs)  # ✅ Décorateur pour enregistrer le modèle
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone')
    search_fields = ('nom', 'email')
