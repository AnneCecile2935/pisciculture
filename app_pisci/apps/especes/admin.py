from django.contrib import admin
from .models import Espece

@admin.register(Espece)
class EspeeAdmin(admin.ModelAdmin):
    list_display = ('nom_commun', 'nom_scientifique', 'est_active')
    list_filter = ('est_active')
    search_fields = ('nom_commun', 'nom_scientifique')
