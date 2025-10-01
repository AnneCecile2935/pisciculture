from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from apps.users import models

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_email_is_required(self):
        with self.assertRaises(ValidationError):
            user = User(email='', username='testuser')
            user.full_clean()

    def test_email_must_be_unique(self):
        User.objects.create_user(
            email='test@example.com',
            username='testuser1',
            password='testpass123'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                username='testuser2',
                password='testpass123'
            )

    def test_invalid_email_format(self):
        with self.assertRaises(ValidationError):
            user = User(email='invalid-email', username='testuser')
            user.full_clean()

    def test_is_staff_sync_with_is_admin(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        user.is_admin = True
        user.save()
        self.assertTrue(user.is_staff)

        user.is_admin = False
        user.save()
        self.assertFalse(user.is_staff)

    def test_str_method(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user), 'test@example.com')

    def test_save_with_empty_email(self):
        user = User(username='testuser')
        with self.assertRaises(ValidationError):
            user.save()
