"""
Configuration Django spécifique aux tests.
Hérite de la configuration principale (settings.py) et surcharge uniquement :
- La base de données (pour utiliser db_test).
- Les paramètres sensibles (SECRET_KEY, DEBUG, etc.).
"""
from .settings import *  # On reprend TOUTE la configuration de base
import os

# =============================================
# Surcharges pour les TESTS
# =============================================
# 1. Base de données : utilise db_test (Docker)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'pisciculture_test'),  # Variable définie dans docker-compose.yml
        'USER': os.getenv('DB_USER', 'test_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'test_password'),
        'HOST': os.getenv('DB_HOST', 'db_test'),  # Nom du service dans docker-compose.yml
        'PORT': os.getenv('DB_PORT', 5432),
    }
}

# 2. Sécurité : désactive les validateurs de mot de passe pour les tests
AUTH_PASSWORD_VALIDATORS = []

# 3. Debug : désactivé pour les tests (optionnel, mais recommandé pour éviter les comportements différents)
DEBUG = False

# 4. Secret Key : utilise une clé factice pour les tests
SECRET_KEY = 'django-insecure-test-key-for-pytest-only'

# 5. Email backend : utilise un backend "en mémoire" pour éviter d'envoyer des emails réels
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# 6. Stockage des fichiers : utilise un stockage en mémoire pour éviter de polluer le système de fichiers
DEFAULT_FILE_STORAGE = 'django.core.files.storage.InMemoryStorage'
