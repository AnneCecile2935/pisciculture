import pytest
from django.conf import settings

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Force l'utilisation de db_test pour les tests."""
    settings.DATABASES["default"]["HOST"] = "db_test"
    settings.DATABASES["default"]["NAME"] = "pisciculture_test"
    settings.DATABASES["default"]["USER"] = "test_user"
    settings.DATABASES["default"]["PASSWORD"] = "test_password"
    with django_db_blocker.unblock():
        yield
