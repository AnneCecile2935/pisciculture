"""
Configuration Django pour le projet de gestion de pisciculture (backend).

Ce fichier centralise tous les paramètres du projet, incluant :
- Les applications installées et leur ordre de chargement.
- La configuration de la base de données (PostgreSQL).
- Les paramètres de sécurité et d'authentification (utilisateurs, mots de passe).
- Les chemins pour les fichiers statiques et médias (uploads).
- Les redirections après connexion/déconnexion.

Pour plus d'informations sur les paramètres disponibles, consulter :
https://docs.djangoproject.com/fr/5.2/topics/settings/
"""

from pathlib import Path
import os
import sys
# =============================================
# CHEMINS DE BASE
# =============================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================
# 2. SÉCURITÉ DE BASE
# =============================================
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%i06ij)%1j(cc45_6gad+pdab-)gw*!zjo7suxddx_@&$y8iau'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
"""
list:
    Liste des noms de domaine/IP autorisés à servir l'application.
    En développement : [] (vide) ou ['localhost', '127.0.0.1'].
    En production : ['ton-domaine.com', 'ip-du-serveur'].
    Exemple pour Docker : ['localhost', 'web'] si ton service s'appelle 'web'.
"""


# =============================================
# 1. APPLICATION DEFINITION
# =============================================

INSTALLED_APPS = [
    # Apps Django par défaut
    'apps.users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps personnalisées (ordre important !)
    'apps.commun',          # Module commun utilisé par d'autres apps
    'apps.sites',          # Gestion des sites/bassins
    'apps.fournisseurs',   # Fournisseurs
    'apps.especes',
    'apps.aliments',
    'apps.activite_quotidien',  # Activités quotidiennes (nourrissage, etc.)
    'apps.stocks',         # Gestion des stocks (aliments, poissons)
    'apps.clients',        # Clients
    'apps.ventes',         # Ventes
]
"""
list:
    Liste de toutes les applications activées dans ce projet Django.
    L'ordre est important :
    - Les apps Django par défaut doivent être en premier.
    - 'apps.users' doit précéder les apps qui dépendent de l'authentification.
    - 'apps.commun' est chargé en premier car il peut contenir des dépendances pour les autres apps.
"""

# =============================================
# 2. PARAMÈTRES CORE (modèles, auth, etc.)
# =============================================
# Modèle User personnalisé
AUTH_USER_MODEL = 'users.User'  # ←--- Doit être défini AVANT DEFAULT_AUTO_FIELD

# Backends d'authentification
AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailAuthBackend',  # Auth par email
    'django.contrib.auth.backends.ModelBackend',  # Auth par défaut (compatible)
]
# Type de champ pour les clés primaires auto-générées
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================
# 3. MIDDLEWARE
# =============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Sécurité (headers HTTP, SSL, etc.)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gestion des sessions
    'django.middleware.common.CommonMiddleware',  # Traitement commun des requêtes
    'django.middleware.csrf.CsrfViewMiddleware',   # Protection CSRF (formulaires)
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Association utilisateur/requête
    'django.contrib.messages.middleware.MessageMiddleware',  # Gestion des messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protection contre le clickjacking
]

# =============================================
# 4. TEMPLATES
# =============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =============================================
# 5. ROUTING
# =============================================
"""
    Chemin vers le module Python contenant les URLs racines du projet.
    Exemple : `core/urls.py` définit les URLs avec `path()`, `include()`, etc.
"""
ROOT_URLCONF = 'core.urls'

"""
    Chemin vers l'application WSGI, utilisée pour servir le projet en production.
    Exemple : utilisé par Gunicorn/UWSGI pour lancer Django.
"""
WSGI_APPLICATION = 'core.wsgi.application'

# =============================================
# 6. DATABASE
# =============================================
TESTING = os.getenv('TESTING', 'false').lower() == 'true'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),

    }
}

# =============================================
# Surcharge pour les tests
# =============================================
if TESTING:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'pisciculture_test'),
        'USER': os.getenv('DB_USER', 'test_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'test_password'),
        'HOST': os.getenv('DB_HOST', 'db_test'),
        'PORT': os.getenv('DB_PORT', '5432'),

    }
# =============================================
# 7. AUTH / SECURITY
# =============================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Vérifie que le mot de passe n'est pas trop similaire aux infos de l'utilisateur
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
     # Vérifie la longueur minimale (8 caractères par défaut)
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Vérifie que le mot de passe n'est pas trop courant (ex: "123456")
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    # Vérifie que le mot de passe n'est pas uniquement numérique
]
"""
list:
    Liste des validateurs appliqués aux mots de passe des utilisateurs.
    Chaque validateur peut lever une `ValidationError` si le mot de passe est invalide.
    Exemple : pour désactiver un validateur en développement, commente la ligne.
"""
# =============================================
# 8. INTERNATIONALIZATION
# =============================================
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# =============================================
# 9. STATIC & MEDIA FILES
# =============================================

STATIC_URL = '/static/'  # URL pour accéder aux fichiers statiques
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Dossier pour les fichiers statiques en production
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')         # Dossier pour les uploads utilisateurs
MEDIA_URL = '/media/'    # URL pour accéder aux fichiers uploadés

# =============================================
# 10. REDIRECTIONS (login/logout)
# =============================================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'dashboard'  # ✅ Après connexion
LOGOUT_REDIRECT_URL = 'login'    # ✅ Après déconnexion
