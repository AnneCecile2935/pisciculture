from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire personnalisé pour la création d'utilisateurs.

    Étend le formulaire standard UserCreationForm pour :
    - Rendre le champ email obligatoire et unique
    - Ajouter une validation spécifique de l'email
    - Inclure les champs is_admin et is_active dès la création
    - Personnaliser les messages d'erreur

    Attributes:
        email (EmailField): Champ email avec validation renforcée.
            Configuré avec :
            - label personnalisé
            - validation obligatoire
            - validateur d'email
            - messages d'erreur personnalisés
    """
    email = forms.EmailField(
        label="Adresse e-mail",
        required=True,
        validators=[EmailValidator(message="Adresse mail invalide")],
        error_messages={
            "required": "L'adresse email est obligatoire.",
            "unique": "Un utilisateur avec cet email existe déjà.",
        }
    )

    class Meta(UserCreationForm.Meta):
        """
        Métadonnées du formulaire.

        Attributes:
            model (Model): Modèle User personnalisé à utiliser
            fields (tuple): Champs à inclure dans le formulaire de création
                Inclut email, username, mots de passe et statuts admin/actif
        """
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active')

class CustomUserAdmin(UserAdmin):
    """
    Configuration personnalisée de l'interface d'administration pour les utilisateurs.

    Étend UserAdmin pour :
    - Utiliser le formulaire personnalisé pour la création
    - Afficher les champs pertinents dans la liste
    - Organiser les champs en sections logiques
    - Permettre la recherche par email et username
    - Trier les utilisateurs par email

    Attributes:
        add_form (Form): Formulaire à utiliser pour la création d'utilisateurs
        list_display (tuple): Champs à afficher dans la liste des utilisateurs
            Inclut :
            - email (str): Adresse email principale
            - username (str): Nom d'utilisateur
            - is_admin (bool): Statut administrateur
            - is_active (bool): Statut actif
            - is_staff (bool): Accès à l'interface admin
            - is_superuser (bool): Super-utilisateur
        list_filter (tuple): Filtres disponibles dans la barre latérale
            Permet de filtrer par statuts et groupes
        fieldsets (tuple): Organisation des champs pour l'édition
            Divisé en sections :
            - Informations principales (email, mot de passe)
            - Permissions (statuts, groupes, permissions)
            - Informations personnelles (username)
        add_fieldsets (tuple): Organisation des champs pour la création
            Version simplifiée pour la création de nouveaux utilisateurs
        search_fields (tuple): Champs utilisables pour la recherche
            Permet de rechercher par email ou username
        ordering (tuple): Tri par défaut des utilisateurs
            Ordre alphabétique par email
    """
    add_form = CustomUserCreationForm
    list_display = ('email', 'username', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_active', 'is_staff', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Informations personnelles', {'fields': ('username',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
