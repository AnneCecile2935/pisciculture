from apps.users import forms
from django.test import TestCase
from apps.users.forms import CustomUserCreationForm
from .factories import UserFactory


class CustomUserCreationFormTests(TestCase):
    def test_form_valid_with_factory_data(self):
        user_data = UserFactory.build()
        form_data = {
            'email': user_data.email,
            'username': user_data.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        user_data = UserFactory.build()
        form_data = {
            'email': 'invalid-email',
            'username': user_data.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_password_mismatch(self):
        user_data = UserFactory.build()
        form_data = {
            'email': user_data.email,
            'username': user_data.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_password_too_short(self):
        user_data = UserFactory.build()
        form_data = {
            'email': user_data.email,
            'username': user_data.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'password1': 'short',
            'password2': 'short'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn("Ce mot de passe est trop court", form.errors['password2'][0])

    def test_form_field_classes(self):
        form = CustomUserCreationForm()
        for field in form.fields:
            self.assertIn('form-control', form.fields[field].widget.attrs['class'])

    def test_form_field_labels(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['email'].label, 'Adresse e-mail')
        self.assertEqual(form.fields['first_name'].label, 'Prénom')
        self.assertEqual(form.fields['last_name'].label, 'Nom')
        self.assertEqual(form.fields['username'].label, 'Nom d\'utilisateur')
        self.assertEqual(form.fields['password1'].label, 'Mot de passe')
        self.assertEqual(form.fields['password2'].label, 'Confirmation du mot de passe')
