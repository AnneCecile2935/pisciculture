from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator

class CustomUserCreationForm(UserCreationForm):
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
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active')

class CustomUserAdmin(UserAdmin):
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
