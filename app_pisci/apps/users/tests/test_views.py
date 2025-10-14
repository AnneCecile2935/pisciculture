import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from apps.users.tests.factories import UserFactory, AdminUserFactory


User = get_user_model()

# --- Tests pour SignupView ---
@pytest.mark.django_db(transaction=True)
def test_signup_view_admin_can_access(admin_user, client):
    """Test : un admin peut accéder à la page de création d'utilisateur."""
    client.force_login(admin_user)
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db(transaction=True)
def test_signup_view_non_admin_redirected(standard_user, client):
    client.force_login(standard_user)
    url = reverse('signup')
    response = client.get(url, follow=True)
    assert response.redirect_chain[0][1] == 302
    assert reverse('login') in response.redirect_chain[0][0]
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert "Seuls les admins peuvent créer des utilisateurs" in str(messages[0])

@pytest.mark.django_db(transaction=True)
def test_signup_view_creates_user(admin_user, client):
    client.force_login(admin_user)
    url = reverse('signup')
    data = {
        'email': 'nouvel@example.com',
        'username': 'nouvel',
        'password1': 'motdepasse123',
        'password2': 'motdepasse123',
    }
    response = client.post(url, data, follow=True)
    assert response.redirect_chain[0][1] == 302  # Vérifie la redirection
    assert reverse('login') in response.redirect_chain[0][0]  # Vérifie l'URL de redirection
    assert User.objects.filter(email='nouvel@example.com').exists()
    messages = list(get_messages(response.wsgi_request))
    assert any("Utilisateur crée avec succès!" in str(message) for message in messages)

@pytest.mark.django_db(transaction=True)
def test_signup_view_fails_without_email(admin_user, client):
    client.force_login(admin_user)
    url = reverse('signup')
    data = {
        'email': '',  # Email manquant
        'username': 'noemailuser',
        'password1': 'motdepasse123',
        'password2': 'motdepasse123',
    }
    response = client.post(url, data)
    assert response.status_code == 200  # Le formulaire est réaffiché
    assert not User.objects.filter(username='noemailuser').exists()
    form = response.context['form']
    assert 'email' in form.errors  # Vérifie que l'erreur est sur le champ email

# --- Tests pour UserViewSet ---
@pytest.mark.django_db(transaction=True)
def test_user_viewset_admin_can_list_users(admin_user, api_client):
    """Test : un admin peut lister les utilisateurs via l'API."""
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db(transaction=True)
def test_user_viewset_non_admin_cannot_list_users(standard_user, api_client):
    """Test : un utilisateur standard ne peut pas lister les utilisateurs via l'API."""
    api_client.force_authenticate(user=standard_user)
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db(transaction=True)
def test_user_viewset_admin_can_delete_user(admin_user, api_client, standard_user):
    """Test : un admin peut supprimer un utilisateur standard."""
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-detail', args=[standard_user.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not User.objects.filter(id=standard_user.id).exists()

@pytest.mark.django_db(transaction=True)
def test_user_viewset_admin_cannot_delete_self(admin_user, api_client):
    """Test : un admin ne peut pas se supprimer lui-même."""
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-detail', args=[admin_user.id])
    response = api_client.delete(url)
    assert response.status_code == 403  # Forbidden
    assert User.objects.filter(id=admin_user.id).exists()

@pytest.mark.django_db(transaction=True)
def test_user_viewset_duplicate_email(admin_user, api_client):
    """Test : la création échoue si l'email est déjà utilisé."""
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-list')
    data = {
        'email': admin_user.email,  # Email déjà utilisé
        'username': 'duplicate',
        'password': 'motdepasse123',
    }
    response = api_client.post(url, data)
    assert response.status_code == 400  # Bad Request
    assert not User.objects.filter(username='duplicate').exists()

# --- Tests pour les contraintes du modèle User ---
@pytest.mark.django_db(transaction=True)
def test_user_email_and_username_unique():
    """Test : email et username doivent être uniques."""
    UserFactory(email="unique@example.com", username="uniqueuser")
    with pytest.raises(IntegrityError):
        UserFactory(email="unique@example.com", username="anotheruser")
    with pytest.raises(IntegrityError):
        UserFactory(email="another@example.com", username="uniqueuser")

@pytest.mark.django_db(transaction=True)
def test_user_email_validation():
    with pytest.raises(ValidationError) as excinfo:
        user = User(email=None, username="testuser")
        user.full_clean()
    assert "Ce champ ne peut pas contenir la valeur nulle" in str(excinfo.value)

@pytest.mark.django_db(transaction=True)
def test_signup_view_fails_with_short_password(admin_user, client):
    """Test : la création échoue si le mot de passe est trop court (< 8 caractères)."""
    client.force_login(admin_user)
    url = reverse('signup')
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password1': '123',  # Trop court
        'password2': '123',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not User.objects.filter(username='testuser').exists()
    form = response.context['form']
    assert "Ce mot de passe est trop court" in str(form.errors['password2'])

@pytest.mark.django_db(transaction=True)
def test_signup_view_fails_with_invalid_email(admin_user, client):
    """Test : la création échoue si l'email est invalide."""
    client.force_login(admin_user)
    url = reverse('signup')
    data = {
        'email': 'invalide',  # Email invalide
        'username': 'testuser',
        'password1': 'motdepasse123',
        'password2': 'motdepasse123',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not User.objects.filter(username='testuser').exists()
    form = response.context['form']
    assert "Saisissez une adresse de courriel valide" in str(form.errors['email'])

@pytest.mark.django_db(transaction=True)
def test_user_viewset_admin_cannot_delete_another_admin(admin_user, api_client):
    """Test : un admin ne peut pas supprimer un autre admin."""
    another_admin = UserFactory(is_admin=True, is_staff=True)
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-detail', args=[another_admin.id])
    response = api_client.delete(url)
    assert response.status_code == 403  # Forbidden
    assert User.objects.filter(id=another_admin.id).exists()

@pytest.mark.django_db(transaction=True)
def test_user_viewset_standard_user_cannot_list_users(standard_user, api_client):
    """Test : un utilisateur standard ne peut pas lister les utilisateurs."""
    api_client.force_authenticate(user=standard_user)
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 403
