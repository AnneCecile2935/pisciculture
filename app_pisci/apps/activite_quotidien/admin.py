from django.contrib import admin
from .models import ReleveTempOxy, Nourrissage

admin.site.register(Nourrissage)
admin.site.register(ReleveTempOxy)

class NourrissageAdmin(admin.ModelAdmin):
    list_display = (
        'code_lot', 'bassin',
        'date_repas', 'qte', 'aliment',
        'site_prod', 'notes'
    )

    def code_lot(self, obj):
        return obj.code_lot
    code_lot.short_description = "Code lot"
