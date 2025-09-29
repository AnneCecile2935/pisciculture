# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    #  Liste des champs à afficher dans l'admin
    list_display = ('email', 'username', 'is_admin', 'is_active', 'is_staff')
    #  Filtres autorisés (remplace is_staff par is_admin)
    list_filter = ('is_admin', 'is_active', 'is_staff', 'groups')
    #  Champs à modifier
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Informations personnelles', {'fields': ('username',)}),
    )
    #  Champs pour la création d'utilisateur
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )
    # Champ utilisé pour la recherche
    search_fields = ('email', 'username')
    # Ordre des champs
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
