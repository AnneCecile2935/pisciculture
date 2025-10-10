import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.users.models import User
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestUserModel:

    def test_email_is_required(self):
        """Test that a user must have an email."""
        user = UserFactory.build(email=None)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_email_must_be_unique(self):
        """Test that user emails must be unique."""
        UserFactory(email="test@example.com")
        with pytest.raises(IntegrityError):
            UserFactory(email="test@example.com")

    def test_email_must_be_valid(self):
        """Test that user email must be a valid format."""
        user = UserFactory.build(email="invalid-email")
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_username_is_required(self):
        """Test that a user must have a username."""
        user = UserFactory.build(username=None)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_username_must_be_unique(self):
        """Test that usernames must be unique."""
        UserFactory(username="unique_username")
        with pytest.raises(IntegrityError):
            UserFactory(username="unique_username")

    def test_is_admin_sets_is_staff(self):
        """Test that setting is_admin=True also sets is_staff=True."""
        user = UserFactory(is_admin=True)
        assert user.is_staff is True

    def test_is_superuser_sets_is_staff(self):
        """Test that setting is_superuser=True also sets is_staff=True."""
        user = UserFactory(is_superuser=True)
        assert user.is_staff is True

    def test_str_method(self):
        """Test the string representation of the user."""
        user = UserFactory(email="test@example.com")
        assert str(user) == "test@example.com"

    def test_save_with_empty_email_raises_error(self):
        """Test that saving a user with no email raises a ValidationError."""
        user = UserFactory.build(email=None)
        with pytest.raises(ValidationError):
            user.save()

    def test_user_can_be_created_with_valid_data(self):
        """Test that a user can be created with valid data."""
        user = UserFactory()
        assert User.objects.filter(email=user.email).exists()

    def test_user_can_update_email(self):
        """Test that a user's email can be updated."""
        user = UserFactory(email="old@example.com")
        user.email = "new@example.com"
        user.save()
        assert User.objects.get(pk=user.pk).email == "new@example.com"

    def test_user_can_update_username(self):
        """Test that a user's username can be updated."""
        user = UserFactory(username="old_username")
        user.username = "new_username"
        user.save()
        assert User.objects.get(pk=user.pk).username == "new_username"

    def test_user_can_be_deleted(self):
        """Test that a user can be deleted."""
        user = UserFactory()
        user_id = user.id
        user.delete()
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user_id)
