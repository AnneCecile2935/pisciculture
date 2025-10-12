import pytest
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIClient

@pytest.fixture
def standard_user():
    return UserFactory(is_admin=False)

@pytest.fixture
def api_client():
    return APIClient()
