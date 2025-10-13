import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from apps.aliments.models import Aliment
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.users.tests.factories import UserFactory
from apps.aliments.tests.factories import AlimentFactory

@pytest.mark.django_db
class TestAlimentListView:
    def test_list_view_with_permission(self, client):
        """Teste l'accès à la liste avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='view_aliment'))
        client.force_login(user)
        AlimentFactory.create_batch(3)
        response = client.get(reverse('aliments:list'))
        assert response.status_code == 200
        assert len(response.context['aliments']) == 3
        assert 'aliments/alim_list.html' in [t.name for t in response.templates]

    def test_list_view_without_permission(self, client):
        """Teste l'accès refusé sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        response = client.get(reverse('aliments:list'))
        assert response.status_code == 403  # Forbidden (raise_exception=True)

    def test_list_view_anonymous(self, client):
        """Teste la redirection vers /login/ pour un utilisateur non connecté."""
        response = client.get(reverse('aliments:list'))
        assert response.status_code == 302
        assert response.url.startswith('/login/')  # Vérifie la redirection

@pytest.mark.django_db
class TestAlimentCreateView:
    def test_create_view_anonymous(self, client):
        """Teste la redirection vers /login/ pour un utilisateur non connecté."""
        response = client.get(reverse('aliments:create'))
        assert response.status_code == 302
        assert response.url.startswith('/login/')

    def test_create_view_with_permission(self, client):
        """Teste la création avec permission et message de succès."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_aliment'))
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.post(reverse('aliments:create'), {
            'nom': 'Nouvel Aliment',
            'code_alim': 'NEW001',
            'fournisseur': fournisseur.id
        })
        assert response.status_code == 302
        assert Aliment.objects.count() == 1
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "L'aliment a été créé avec succès" in str(messages[0])

    def test_create_view_invalid_data(self, client):
        """Teste la soumission de données invalides."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_aliment'))
        client.force_login(user)
        response = client.post(reverse('aliments:create'), {
            'nom': '',  # Champ obligatoire manquant
            'code_alim': 'NEW001',
            'fournisseur': FournisseurFactory().id
        })
        assert response.status_code == 200  # Re-affiche le formulaire
        assert 'aliments/alim_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestAlimentUpdateView:
    def test_update_view_with_permission(self, client):
        """Teste la mise à jour avec permission et message de succès."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_aliment'))
        client.force_login(user)
        aliment = AlimentFactory(nom="Ancien Nom")
        response = client.post(reverse('aliments:update', args=[aliment.id]), {
            'nom': 'Nouveau Nom',
            'code_alim': aliment.code_alim,
            'fournisseur': aliment.fournisseur.id
        })
        assert response.status_code == 302
        aliment.refresh_from_db()
        assert aliment.nom == 'Nouveau Nom'
        messages = list(get_messages(response.wsgi_request))
        assert "L'aliment a été mis à jour avec succès" in str(messages[0])

@pytest.mark.django_db
class TestAlimentDeleteView:
    def test_delete_view_with_permission(self, client):
        from django.contrib.contenttypes.models import ContentType
        """Teste la suppression avec permission."""
        user = UserFactory(is_staff=True)
        content_type = ContentType.objects.get_for_model(Aliment)
        permission, _ = Permission.objects.get_or_create(
            codename='delete_aliment',
            content_type=content_type,
            defaults={'name': 'Can delete aliment'}
        )
        user.user_permissions.add(permission)
        user.save()

        client.force_login(user)
        aliment = AlimentFactory(code_alim="TEST01")

        # Vérifie que l'aliment existe avant suppression
        assert Aliment.objects.filter(pk=aliment.pk).exists()

        response = client.post(reverse('aliments:delete', args=[aliment.id]), follow=True)

        # Vérifie que l'aliment a été supprimé
        assert not Aliment.objects.filter(pk=aliment.pk).exists()
        assert response.status_code == 200

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "L'aliment a été supprimé avec succès" in str(messages[0])

    def test_delete_view_anonymous(self, client):
        """Teste la redirection vers /login/ pour un utilisateur non connecté."""
        aliment = AlimentFactory(code_alim="TEST01")
        response = client.get(reverse('aliments:delete', args=[aliment.id]))
        assert response.status_code == 302
        assert response.url.startswith('/login/')
