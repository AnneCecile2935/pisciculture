from django.contrib import admin
from .models import Fournisseurs

admin.site.register(Fournisseurs)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'get_type_fournisseur_display', 'est_actif')
    list_filter = ('type_fournisseur', 'est_actif')
    search_fields = ('nom', 'ville', 'contact')
