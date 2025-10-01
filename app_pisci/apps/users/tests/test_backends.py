from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from ..backends import EmailAuthBackend
from .factories import UserFactory

User = get_user_model()

class EmailAuthBackendTests(TestCase):
    def setUp(self):
        self.backend = EmailAuthBackend()
        self.request = RequestFactory().get('/fake-path')
        self.user = UserFactory()
        self.user.set_password('testpass123')
        self.user.save()

    def test_authenticate_with_valid_email_and_password(self):
        user = self.backend.authenticate(self.request, username=self.user.email, password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)

    def test_authenticate_with_invalid_email(self):
        user = self.backend.authenticate(self.request, username='invalid@example.com', password='testpass123')
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        user = self.backend.authenticate(self.request, username=self.user.email, password='wrongpassword')
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        user = self.backend.authenticate(self.request, username='nonexistent@example.com', password='testpass123')
        self.assertIsNone(user)

    def test_authenticate_with_empty_credentials(self):
        user = self.backend.authenticate(self.request, username='', password='')
        self.assertIsNone(user)

    def test_get_user(self):
        user = self.backend.get_user(self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
