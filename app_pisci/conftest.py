import pytest
from django.conf import settings
from apps.users.tests.factories import UserFactory, AdminUserFactory
from apps.stocks.tests.factories import LotDePoissonFactory
from rest_framework.test import APIClient
from django.test import Client
from django.db import transaction

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Fixture pour activer l'accès à la base de données pour tous les tests.
    """
    pass

@pytest.fixture
def db_transactional(db):
    """
    Fixture pour encapsuler chaque test dans une transaction qui est annulée à la fin.
    """
    with transaction.atomic():
        yield db
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Force l'utilisation de db_test pour les tests."""
    settings.DATABASES["default"]["HOST"] = "db_test"
    settings.DATABASES["default"]["NAME"] = "pisciculture_test"
    settings.DATABASES["default"]["USER"] = "test_user"
    settings.DATABASES["default"]["PASSWORD"] = "test_password"
    with django_db_blocker.unblock():
        yield

@pytest.fixture
def admin_user(db):
    user = AdminUserFactory()
    assert user.is_admin is True
    assert user.is_staff is True
    return user

@pytest.fixture
def standard_user(db):
    return UserFactory()

@pytest.fixture
def client(db):
    return Client()

@pytest.fixture
def api_client(db):
    return APIClient()

@pytest.fixture
def lot_factory(db):
    return LotDePoissonFactory

@pytest.fixture
def normal_user(db):
    return UserFactory(is_admin=False, is_staff=False)
