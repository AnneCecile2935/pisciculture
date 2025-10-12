import pytest
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer
from apps.users.tests.factories import UserFactory, AdminUserFactory
from rest_framework import serializers

User = get_user_model()

@pytest.mark.django_db
class TestUserSerializer:
    def test_serializer_create_user(self):
        """Test : création d'un utilisateur via le serializer."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'validpassword123'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'newuser@example.com'
        assert user.check_password('validpassword123')  # Vérifie que le mot de passe est haché
        assert user.is_admin is False  # Valeur par défaut

    def test_serializer_hash_password_on_create(self):
        """Test : le mot de passe est bien haché à la création."""
        data = {
            'email': 'user2@example.com',
            'username': 'user2',
            'password': 'mypassword123'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.password != 'mypassword123'  # Le mot de passe doit être haché
        assert user.check_password('mypassword123')

    def test_serializer_hash_password_on_update(self):
        """Test : le mot de passe est haché lors de la mise à jour."""
        user = UserFactory(password='oldpassword123')
        data = {'password': 'newpassword123'}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.check_password('newpassword123')

    def test_serializer_password_write_only(self):
        """Test : le mot de passe n'est jamais renvoyé dans la réponse."""
        user = UserFactory(password='mypassword123')
        serializer = UserSerializer(instance=user)
        assert 'password' not in serializer.data

    def test_serializer_is_admin_read_only(self):
        user = UserFactory()
        data = {'is_admin': True}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        with pytest.raises(serializers.ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        print(excinfo.value.detail)  # ← Affiche le dictionnaire d'erreurs
        assert 'is_admin' in excinfo.value.detail
        # assert excinfo.value.detail['is_admin'][0] == 'Seul un administrateur peut modifier ce champ'

    def test_serializer_is_staff_read_only(self):
        """Test : is_staff ne peut pas être modifié via le serializer."""
        user = UserFactory()
        data = {'is_staff': True}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        with pytest.raises(serializers.ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert 'is_staff' in excinfo.value.detail
        assert excinfo.value.detail['is_staff'][0] == 'Ce champ ne peut pas être modifié via l\'API'


    def test_serializer_required_fields(self):
        """Test : les champs obligatoires sont bien validés."""
        data = {}  # Données vides
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'required' in str(serializer.errors['email'])
        assert 'required' in str(serializer.errors['username'])
        assert 'required' in str(serializer.errors['password'])

    def test_serializer_password_min_length(self):
        """Test : validation de la longueur minimale du mot de passe."""
        data = {
            'email': 'user@example.com',
            'username': 'user',
            'password': 'short'  # Trop court
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'min_length' in str(serializer.errors['password'])

    def test_serializer_email_validation(self):
        """Test : validation du format de l'email."""
        data = {
            'email': 'invalid-email',
            'username': 'user',
            'password': 'validpassword123'
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'invalid' in str(serializer.errors['email'])

    def test_serializer_username_required(self):
        """Test : username est obligatoire."""
        data = {
            'email': 'user@example.com',
            'password': 'validpassword123'
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'required' in str(serializer.errors['username'])

    def test_serializer_exclude_password_from_response(self):
        """Test : le mot de passe est exclu de la réponse JSON."""
        user = UserFactory(password='mypassword123')
        serializer = UserSerializer(instance=user)
        assert 'password' not in serializer.data
        assert serializer.data['email'] == user.email
        assert serializer.data['is_admin'] == user.is_admin

    def test_serializer_partial_update_without_password(self):
        """Test : mise à jour partielle sans mot de passe."""
        user = UserFactory(password='oldpassword123')
        data = {'first_name': 'Updated'}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.first_name == 'Updated'
        assert updated_user.check_password('oldpassword123')  # Le mot de passe reste inchangé

    def test_serializer_cannot_set_is_admin(self):
        """Test : un utilisateur normal ne peut pas devenir admin via le serializer."""
        user = UserFactory()
        data = {'is_admin': True}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        with pytest.raises(serializers.ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert 'is_admin' in excinfo.value.detail

    def test_serializer_admin_can_update_other_fields(self):
        """Test : un admin peut mettre à jour d'autres champs (sauf is_admin/is_staff)."""
        user = UserFactory()
        data = {'first_name': 'Updated', 'email': 'newemail@example.com'}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.first_name == 'Updated'
        assert updated_user.email == 'newemail@example.com'
