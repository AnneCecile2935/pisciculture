import pytest
from django.conf import settings
from tests.factories import UserFactory, AdminUserFactory
from rest_framework.test import APIClient
from django.test import Client

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
    return AdminUserFactory()

@pytest.fixture
def standard_user(db):
    return UserFactory()

@pytest.fixture
def client(db):
    return Client()

@pytest.fixture
def api_client(db):
    return APIClient()
