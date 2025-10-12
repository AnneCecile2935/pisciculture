# Documentation des Tests - Pisciculture

Ce document décrit comment lancer, comprendre et étendre les tests du projet **Pisciculture**.

---

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Structure des Tests](#structure-des-tests)
3. [Lancer les Tests](#lancer-les-tests)
   - [Tous les tests](#tous-les-tests)
   - [Tests spécifiques](#tests-spécifiques)
   - [Rapport de Coverage](#rapport-de-coverage)
4. [Composants Testés](#composants-testés)
   - [Modèles](#modèles)
   - [Vues](#vues)
   - [Formulaires](#formulaires)
   - [Serializers](#serializers)
   - [Backend d'Authentification](#backend-dauthentification)
5. [Ajouter un Nouveau Test](#ajouter-un-nouveau-test)
6. [Bonnes Pratiques](#bonnes-pratiques)
7. [CI/CD](#cicd)
8. [Dépannage](#dépannage)

---

## Prérequis
- **Docker** et **docker-compose** installés.
- Le projet démarré avec :
  ```bash
  docker-compose up -d

## Structure des Tests
Les tests sont organisés dans le dossier apps/ selon la structure suivante :
 Copierapps/
├── users/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py        # Tests des modèles User
│   │   ├── test_views.py         # Tests des vues (API/HTML)
│   │   ├── test_forms.py         # Tests des formulaires
│   │   ├── test_serializers.py   # Tests des serializers DRF
│   │   ├── test_backends.py      # Tests du backend d'auth
│   │   └── factories.py          # Factories pour <followup encodedFollowup="%7B%22snippet%22%3A%22Fact

## Lancer les tests

```bash
docker-compose exec web pytest
```

## Tests spécifiques
| Composant          | Commande                                      | Description                                  |
|--------------------|-----------------------------------------------|----------------------------------------------|
| **Modèle `User`**  | `docker-compose exec web pytest apps/users/tests/test_models.py`      | Tests du modèle utilisateur (création, permissions, validations). |
| **Vues**           | `docker-compose exec web pytest apps/users/tests/test_views.py`       | Tests des vues (authentification, création d'utilisateur, permissions). |
| **Formulaires**    | `docker-compose exec web pytest apps/users/tests/test_forms.py`       | Tests des formulaires (`CustomAuthenticationForm`, `CustomUserCreationForm`). |
| **Serializers**    | `docker-compose exec web pytest apps/users/tests/test_serializers.py` | Tests des serializers DRF (création, mise à jour, validations). |
| **Backend d'auth** | `docker-compose exec web pytest apps/users/tests/test_backends.py`   | Tests du backend d'authentification (`EmailAuthBackend`). |
| **Tous les tests** | `docker-compose exec web pytest apps/users/tests/`                   | Lance tous les tests pour l'app `users`. |
| **Coverage**       | `docker-compose exec web pytest --cov=apps/users --cov-report=html`  | Génère un rapport de coverage HTML. |


## Rapport de Coverage

```bash
docker-compose exec web pytest --cov=apps/users --cov-report=html
```
- Ouvre htmlcov/index.html dans ton navigateur pour voir les résultats.

## Composants testés

### Modèles

- User :

- Création, validation des champs (email, username, password).
- Permissions (is_admin, is_staff).
- Méthodes custom (ex: save()).


- Exemple :
 ```bash
 def test_user_creation():
    user = UserFactory(email="test@example.com")
    assert user.email == "test@example.com"
```


### Vues

- Authentification (LoginView, LogoutView).
- Création d'utilisateur (UserCreateView).
- Permissions (accès réservé aux admins).
- Exemple :
```bash
	def test_login_view(client):
    response = client.post('/login/', {'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 200
```

### Formulaires

- CustomAuthenticationForm :

- Validation avec email/mot de passe.
- Messages d'erreur personnalisés.


- CustomUserCreationForm :

- Correspondance des mots de passe.
- Longueur minimale du mot de passe (8 caractères).



### Serializers

- UserSerializer :

- Hachage du mot de passe (make_password).
- Champs en lecture seule (is_admin, is_staff).
- Validation des données d'entrée.



- Backend d'Authentification

- EmailAuthBackend :

- Authentification par email (pas par username).
- Gestion des utilisateurs inactifs.
- Intégration avec Django (AUTHENTICATION_BACKENDS).

## Ajouter un Nouveau Test

- Crée un fichier dans apps/<app>/tests/ (ex: test_bassin.py).
- Utilise les factories pour générer des données :
```bash
from apps.users.tests.factories import UserFactory, AdminUserFactory
user = UserFactory()  # Crée un utilisateur standard
admin = AdminUserFactory()  # Crée un admin
```

- Structure recommandée :
```bash
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestNouveauComposant:
    def test_cas_nominal(self):
        # Test du cas idéal
        pass

    def test_cas_erreur(self):
        # Test des erreurs (ex: données invalides)
        pass
```


## Bonnes Pratiques

- Isolation : Chaque test doit être indépendant (utilise @pytest.mark.django_db pour les tests nécessitant la base de données).
- Nommage :

Fichiers : test_<composant>.py (ex: test_bassin.py).
Méthodes : test_<comportement> (ex: test_bassin_creation).


- Assertions claires :
```bash
# ✅ Bien
assert user.is_active is True

# ❌ À éviter
assert user.is_active

```

- Utilise Factory Boy pour éviter les données en dur :
 bassin = BassinFactory(site=site, nom="Bassin 1")



- CI/CD
- Configuration GitHub Actions
- Crée un fichier .github/workflows/tests.yml :
```bash
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker-compose up -d
      - run: docker-compose exec web pytest --cov=apps/users
```

- Badge de Coverage
- Ajoute un badge à ton README.md (ex: avec Codecov) :
 Copier[![Coverage Status](https://img.shields.io/codecov/c/github/ton-org/pisciculture)](https://codecov.io/gh/ton-org/pisciculture)

## Dépannage

| Problème                          | Solution                                                                 |
|-----------------------------------|--------------------------------------------------------------------------|
| `docker-compose exec web pytest` échoue | Vérifie que les containers sont démarrés : `docker-compose ps`.         |
| Erreur de base de données         | Lance les migrations : `docker-compose exec web python manage.py migrate`. |
| Tests lents                       | Utilise `--disable-warnings` ou `-x` pour arrêter au premier échec.     |
| Coverage insuffisant              | Ajoute des tests pour les lignes manquantes (voir `htmlcov/index.html`). |
| Erreur de connexion à la base     | Vérifie que `db` est `healthy` : `docker-compose ps`.                   |
| Erreur de syntaxe Python          | Lance un linter : `docker-compose exec web flake8`.                     |



📌 Notes Supplémentaires

Tests end-to-end : Pour les flux complets (ex: création d'un bassin + ajout de poissons), utilise pytest-django avec des requêtes HTTP réelles.
Données de test : Les factories sont dans apps/<app>/tests/factories.py. Ajoute-y des modèles métiers (ex: BassinFactory).
Environnement de test : Une base de données dédiée (db_test) est utilisée pour éviter les conflits avec la production.
