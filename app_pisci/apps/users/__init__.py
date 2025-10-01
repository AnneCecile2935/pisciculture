"""Quand on charge l’application users, utilise la classe UsersConfig
(dans apps.py) comme configuration, et pas la configuration par défaut.
"""

default_app_config = 'apps.users.apps.UsersConfig'
