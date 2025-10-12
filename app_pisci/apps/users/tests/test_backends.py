import pytest
from django.contrib.auth import get_user_model
from apps.users.backends import EmailAuthBackend
from apps.users.tests.factories import UserFactory

User = get_user_model()

@pytest.mark.django_db
class TestEmailAuthBackend:
    def test_authenticate_with_valid_email_and_password(self):
        """Test : authentification réussie avec email/mot de passe valides."""
        user = UserFactory(password="mypassword123")
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=user.email,
            password="mypassword123"
        )
        assert authenticated_user == user

    def test_authenticate_with_wrong_password(self):
        """Test : échec si le mot de passe est incorrect."""
        user = UserFactory(password="mypassword123")
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=user.email,
            password="wrongpassword"
        )
        assert authenticated_user is None

    def test_authenticate_with_nonexistent_email(self):
        """Test : échec si l'email n'existe pas."""
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username="nonexistent@example.com",
            password="mypassword123"
        )
        assert authenticated_user is None

    def test_authenticate_with_username_instead_of_email(self):
        """Test : échec si on utilise le username au lieu de l'email."""
        user = UserFactory(password="mypassword123")
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=user.username,  # ← On passe le username au lieu de l'email
            password="mypassword123"
        )
        assert authenticated_user is None

    def test_authenticate_with_inactive_user(self):
        """Test : échec si l'utilisateur est inactif."""
        user = UserFactory(password="mypassword123", is_active=False)
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=user.email,
            password="mypassword123"
        )
        assert authenticated_user is None

    def test_authenticate_with_missing_password(self):
        """Test : échec si le mot de passe est None."""
        user = UserFactory(password="mypassword123")
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=user.email,
            password=None
        )
        assert authenticated_user is None

    def test_authenticate_with_missing_email(self):
        """Test : échec si l'email est None."""
        backend = EmailAuthBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username=None,
            password="mypassword123"
        )
        assert authenticated_user is None

    def test_get_user(self):
        """Test : la méthode get_user fonctionne correctement."""
        user = UserFactory()
        backend = EmailAuthBackend()
        fetched_user = backend.get_user(user.id)
        assert fetched_user == user

    def test_get_user_with_invalid_id(self):
        """Test : get_user retourne None pour un ID invalide."""
        backend = EmailAuthBackend()
        fetched_user = backend.get_user(999999)  # ID qui n'existe pas
        assert fetched_user is None
