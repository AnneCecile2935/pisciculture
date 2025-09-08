from django.contrib import admin
from .models import Site, Bassin, ReleveTempOxy

# Register your models here.
admin.site.register(Site)
admin.site.register(Bassin)
admin.site.register(ReleveTempOxy)
