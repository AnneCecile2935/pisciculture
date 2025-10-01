from django.test import TestCase
from apps.users.serializers import UserSerializer
from .factories import UserFactory
from django.core.exceptions import ValidationError
import apps.users.serializers

class UserSerializerTests(TestCase):
    def test_serializer_with_valid_data(self):
        user = UserFactory.build()
        serializer = UserSerializer(instance=user)
        self.assertEqual(serializer.data['email'], user.email)
        self.assertEqual(serializer.data['username'], user.username)
        self.assertEqual(serializer.data['first_name'], user.first_name)
        self.assertEqual(serializer.data['last_name'], user.last_name)
        self.assertNotIn('password', serializer.data)  # Vérifie que le mot de passe n'est pas dans la réponse

    def test_serializer_create_user(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpass123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password('testpass123'))  # Vérifie que le mot de passe est bien haché

    def test_serializer_password_min_length(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'short'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Le mot de passe doit contenir au moins 8 caractères", str(serializer.errors['password']))

    def test_serializer_missing_required_fields(self):
        data = {
            'email': 'test@example.com',
            # 'username' est manquant
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpass123'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Un nom d'utilisateur est obligatoire", str(serializer.errors['username']))

    def test_serializer_update_user(self):
        user = UserFactory()
        data = {
            'email': 'newemail@example.com',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'password': 'newpassword123'
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertTrue(updated_user.check_password('newpassword123'))

    def test_serializer_read_only_fields(self):
        user = UserFactory()
        data = {
            'is_admin': True  # On essaie de modifier un champ en lecture seule
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())  # Le serializer doit être valide, mais le champ `is_admin` ne doit pas être modifié
        updated_user = serializer.save()
        self.assertEqual(updated_user.is_admin, user.is_admin)  # Vérifie que `is_admin` n'a pas changé
