import pytest
from django import forms
from apps.users.forms import CustomAuthenticationForm, CustomUserCreationForm
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestCustomAuthenticationForm:
    def test_form_valid_with_email(self):
        """Test : le formulaire accepte un email comme username."""
        user = UserFactory(password="mypassword123")
        form_data = {
            'username': user.email,  # ← On utilise l'email
            'password': "mypassword123"
        }
        form = CustomAuthenticationForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_with_wrong_password(self):
        """Test : formulaire invalide avec un mot de passe incorrect."""
        user = UserFactory(password="mypassword123")
        form_data = {'username': user.email, 'password': "wrongpassword"}
        form = CustomAuthenticationForm(data=form_data)
        assert not form.is_valid()
        assert "Saisissez un Nom d" in str(form.errors)  # ← Vérifie seulement le début
        assert "mot de passe valides" in str(form.errors)  # ← Vérifie la fin

    def test_form_invalid_with_nonexistent_email(self):
        form_data = {'username': "unknown@example.com", 'password': "mypassword123"}
        form = CustomAuthenticationForm(data=form_data)
        assert not form.is_valid()
        assert "Saisissez un Nom d" in str(form.errors)
        assert "mot de passe valides" in str(form.errors)

    def test_form_has_email_field(self):
        """Test : le champ username est bien labellisé 'Adresse email'."""
        form = CustomAuthenticationForm()
        assert form.fields['username'].label == "Adresse email"

    def test_form_fields_have_css_class(self):
        """Test : tous les champs ont la classe 'form-control'."""
        form = CustomAuthenticationForm()
        for field in form.fields:
            assert 'form-control' in form.fields[field].widget.attrs['class']

@pytest.mark.django_db
class TestCustomUserCreationForm:
    def test_form_valid(self):
        """Test : formulaire valide avec des données correctes."""
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'validpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_password_mismatch(self):
        """Test : formulaire invalide si les mots de passe ne correspondent pas."""
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'password123',
            'password2': 'differentpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "Les mots de passe ne correspondent pas." in str(form.errors['password2'])

    def test_form_invalid_password_too_short(self):
        """Test : formulaire invalide si le mot de passe est trop court."""
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'short',
            'password2': 'short'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "Ce mot de passe est trop court." in str(form.errors['password2'])

    def test_form_saves_user(self):
        """Test : le formulaire sauvegarde correctement un utilisateur."""
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'validpassword123',
            'password2': 'validpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.email == 'newuser@example.com'
        assert user.check_password('validpassword123')

    def test_form_fields_have_css_class(self):
        """Test : tous les champs ont la classe 'form-control'."""
        form = CustomUserCreationForm()
        for field in form.fields:
            assert 'form-control' in form.fields[field].widget.attrs['class']

    def test_form_fields_have_custom_labels(self):
        """Test : les labels des champs sont personnalisés."""
        form = CustomUserCreationForm()
        assert form.fields['email'].label == 'Adresse e-mail'
        assert form.fields['first_name'].label == 'Prénom'
        assert form.fields['last_name'].label == 'Nom'
        assert form.fields['username'].label == "Nom d'utilisateur"
        assert form.fields['password1'].label == 'Mot de passe'
        assert form.fields['password2'].label == 'Confirmation du mot de passe'
