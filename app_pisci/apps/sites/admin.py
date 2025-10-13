from django.contrib import admin
from .models import Site, Bassin

admin.site.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'est_actif', 'created_at')
    list_filter = ('est_actif',)
    search_fields = ('nom',)
    ordering = ('-created_at',)

admin.site.register(Bassin)
class BassinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site', 'volume', 'type', 'est_actif', 'created_at')
    list_filter = ('site', 'type', 'est_actif')
    search_fields = ('nom', 'type')
    ordering = ('-created_at',)
