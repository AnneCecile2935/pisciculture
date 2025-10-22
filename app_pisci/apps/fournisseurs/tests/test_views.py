import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from apps.fournisseurs.models import Fournisseur
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestFournisseurListView:
    def test_fournisseur_list_view_with_permission(self, client):
        """Teste l'accès à la liste avec les permissions requises."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='view_fournisseur'))
        client.force_login(user)
        FournisseurFactory.create_batch(3)
        response = client.get(reverse('fournisseurs:fournisseur-list'))
        assert response.status_code == 200
        assert len(response.context['fournisseurs']) == 3
        assert 'fournisseurs/frs_list.html' in [t.name for t in response.templates]

    def test_fournisseur_list_view_without_permission(self, client):
        """Teste l'accès refusé sans permission."""
        user = UserFactory(is_staff=True)  # Pas de permission
        client.force_login(user)
        response = client.get(reverse('fournisseurs:fournisseur-list'))
        assert response.status_code == 403  # Forbidden

    def test_fournisseur_list_view_anonymous(self, client):
        """Teste l'accès refusé pour un utilisateur non connecté."""
        response = client.get(reverse('fournisseurs:fournisseur-list'))
        assert response.status_code == 302  # Redirection vers login

@pytest.mark.django_db
class TestFournisseurCreateView:
    def test_fournisseur_create_view_with_permission(self, client):
        """Teste la création d'un fournisseur avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_fournisseur'))
        client.force_login(user)
        response = client.post(reverse('fournisseurs:fournisseur-create'), {
            'nom': 'Nouveau Fournisseur',
            'adresse': '123 Rue Test',
            'ville': 'Testville',
            'code_postal': '35000',
            'type_fournisseur': 'ALIMENT',
            'est_actif': True
        })
        assert response.status_code == 302  # Redirection après succès
        assert Fournisseur.objects.count() == 1
        assert response.url == reverse('fournisseurs:fournisseur-list')

    def test_fournisseur_create_view_without_permission(self, client):
        """Teste le refus de création sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        response = client.post(reverse('fournisseurs:fournisseur-create'), {
            'nom': 'Fournisseur Interdit',
            'adresse': '456 Rue Test',
            'ville': 'Testville',
            'code_postal': '35000',
            'type_fournisseur': 'ALIMENT',
        })
        assert response.status_code == 403  # Forbidden

    def test_fournisseur_create_view_invalid_data(self, client):
        """Teste la soumission de données invalides."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_fournisseur'))
        client.force_login(user)
        response = client.post(reverse('fournisseurs:fournisseur-create'), {
            'nom': '',  # Champ obligatoire manquant
            'adresse': '123 Rue Test',
            'ville': 'Testville',
            'code_postal': '35000',
            'type_fournisseur': 'ALIMENT',
        })
        assert response.status_code == 200  # Re-affiche le formulaire avec erreurs
        assert "Ce champ est obligatoire" in response.content.decode('utf-8')

    def test_fournisseur_create_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_fournisseur'))
        client.force_login(user)
        response = client.get(reverse('fournisseurs:fournisseur-create'))
        assert response.status_code == 200
        assert 'fournisseurs/frs_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestFournisseurUpdateView:
    def test_fournisseur_update_view_with_permission(self, client):
        """Teste la mise à jour avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_fournisseur'))
        client.force_login(user)
        fournisseur = FournisseurFactory(nom='Ancien Nom')
        response = client.post(reverse('fournisseurs:fournisseur-update', args=[fournisseur.id]), {
            'nom': 'Nouveau Nom',
            'adresse': fournisseur.adresse,
            'ville': fournisseur.ville,
            'code_postal': fournisseur.code_postal,
            'type_fournisseur': fournisseur.type_fournisseur,
            'est_actif': False
        })
        assert response.status_code == 302
        fournisseur.refresh_from_db()
        assert fournisseur.nom == 'Nouveau Nom'
        assert fournisseur.est_actif is False

    def test_fournisseur_update_view_without_permission(self, client):
        """Teste le refus de mise à jour sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.post(reverse('fournisseurs:fournisseur-update', args=[fournisseur.id]), {
            'nom': 'Nom Interdit',
            'adresse': fournisseur.adresse,
            'ville': fournisseur.ville,
            'code_postal': fournisseur.code_postal,
            'type_fournisseur': fournisseur.type_fournisseur,
        })
        assert response.status_code == 403  # Forbidden

    def test_fournisseur_update_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_fournisseur'))
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.get(reverse('fournisseurs:fournisseur-update', args=[fournisseur.id]))
        assert response.status_code == 200
        assert 'fournisseurs/frs_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestFournisseurDeleteView:
    def test_fournisseur_delete_view_with_permission(self, client):
        """Teste la suppression avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_fournisseur'))
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.post(reverse('fournisseurs:fournisseur-delete', args=[fournisseur.id]))
        assert response.status_code == 302
        assert Fournisseur.objects.count() == 0
        assert response.url == reverse('fournisseurs:fournisseur-list')

    def test_fournisseur_delete_view_without_permission(self, client):
        """Teste le refus de suppression sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.post(reverse('fournisseurs:fournisseur-delete', args=[fournisseur.id]))
        assert response.status_code == 403  # Forbidden

    def test_fournisseur_delete_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_fournisseur'))
        client.force_login(user)
        fournisseur = FournisseurFactory()
        response = client.get(reverse('fournisseurs:fournisseur-delete', args=[fournisseur.id]))
        assert response.status_code == 200
        assert 'fournisseurs/frs_confirm_delete.html' in [t.name for t in response.templates]
