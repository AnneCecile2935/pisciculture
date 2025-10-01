from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .factories import UserFactory

User = get_user_model()

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_access_denied_for_non_admin(self):
        user = UserFactory(is_admin=False)
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_access_granted_for_admin(self):
        admin = UserFactory(is_admin=True)
        self.client.force_login(admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_signup(self):
        admin = UserFactory(is_admin=True)
        self.client.force_login(admin)
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_success_message(self):
        admin = UserFactory(is_admin=True)
        self.client.force_login(admin)
        form_data = {
            'email': 'messageuser@example.com',
            'username': 'messageuser',
            'first_name': 'Message',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.url, data=form_data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        self.assertTrue(User.objects.filter(email='messageuser@example.com').exists())

    def test_invalid_form_data(self):
        admin = UserFactory(is_admin=True)
        self.client.force_login(admin)
        form_data = {
            'email': 'invalid-email',
            'username': 'invaliduser',
            'first_name': 'Invalid',
            'last_name': 'User',
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='invaliduser').exists())

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = UserFactory(is_admin=True)
        self.client.force_authenticate(user=self.admin)
        self.list_url = reverse('user-list')

    def test_create_user(self):
        data = {
            'email': 'apiuser@example.com',
            'username': 'apiuser',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'testpass123'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='apiuser@example.com').exists())

    def test_non_admin_cannot_create_user(self):
        user = UserFactory(is_admin=False)
        self.client.force_authenticate(user=user)
        data = {
            'email': 'unauthorized@example.com',
            'username': 'unauthorized',
            'first_name': 'Unauthorized',
            'last_name': 'User',
            'password': 'testpass123'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_self_forbidden(self):
        user_to_delete = UserFactory()
        self.client.force_authenticate(user=user_to_delete)
        detail_url = reverse('user-detail', args=[user_to_delete.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Vous ne pouvez pas supprimer votre propre compte")

    def test_delete_other_user(self):
        admin = UserFactory(is_admin=True)
        user_to_delete = UserFactory()
        self.client.force_authenticate(user=admin)
        detail_url = reverse('user-detail', args=[user_to_delete.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user_to_delete.id).exists())

class LoginRedirectTests(TestCase):
    def test_login_redirects_to_dashboard(self):
        user = UserFactory()
        user.set_password('testpass123')
        user.save()
        client = Client()
        login_url = reverse('login')
        response = client.post(login_url, {'username': user.email, 'password': 'testpass123'}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
