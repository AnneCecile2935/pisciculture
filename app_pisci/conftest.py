import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission

from apps.users.tests.factories import UserFactory, AdminUserFactory
from apps.aliments.tests.factories import AlimentFactory
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.stocks.tests.factories import LotDePoissonFactory


# ======================
# CLIENTS
# ======================

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def api_client():
    return APIClient()


# ======================
# USERS
# ======================

@pytest.fixture
def standard_user(db):
    return UserFactory(password="securepassword123")


@pytest.fixture
def admin_user(db):
    user = AdminUserFactory(password="securepassword123")
    return user


@pytest.fixture
def staff_user(db):
    return UserFactory(password="securepassword123", is_staff=True)


# ======================
# FACTORIES
# ======================

@pytest.fixture
def aliment_factory():
    return AlimentFactory

@pytest.fixture
def fournisseur_factory():
    return FournisseurFactory

@pytest.fixture
def lot_factory():
    return LotDePoissonFactory


# ======================
# OBJECTS READY TO USE
# ======================

@pytest.fixture
def fournisseur(db):
    return FournisseurFactory()

@pytest.fixture
def aliment(db, fournisseur):
    return AlimentFactory(fournisseur=fournisseur)

@pytest.fixture
def aliments(db, fournisseur):
    return AlimentFactory.create_batch(3, fournisseur=fournisseur)


# ======================
# PERMISSIONS (IMPORTANT)
# ======================

@pytest.fixture
def perm_add_aliment(db):
    return Permission.objects.get(codename="add_aliment")

@pytest.fixture
def perm_change_aliment(db):
    return Permission.objects.get(codename="change_aliment")

@pytest.fixture
def perm_delete_aliment(db):
    return Permission.objects.get(codename="delete_aliment")


# ======================
# AUTH HELPERS (OPTIONNEL MAIS PROPRE)
# ======================

@pytest.fixture
def login(client):
    def _login(user):
        client.force_login(user)
        return client
    return _login
