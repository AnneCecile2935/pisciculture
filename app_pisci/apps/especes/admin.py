from django.contrib import admin
from .models import Espece

@admin.register(Espece)
class EspeeAdmin(admin.ModelAdmin):
    list_display = ('nom_commun', 'nom_scientifique', 'est_actif')
    list_filter = ('est_actif',)
    search_fields = ('nom_commun', 'nom_scientifique')
