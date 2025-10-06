from django.contrib import admin
from .models import Aliment

@admin.register(Aliment)
class AlimentAdmin(admin.ModelAdmin):
    list_display = ("code_alim", "nom", "fournisseur")
    search_fields = ("code_alim", "nom")
    list_filter = ("fournisseur",)
