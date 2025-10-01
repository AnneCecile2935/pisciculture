# Permet à Django de reconnaître l'app et d’appliquer les configurations spécifiques (ex: default_auto_field).

from django.apps import AppConfig
#AppConfig est une classe de base fournie par Django pour configurer une application.

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
