import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from apps.especes.models import Espece
from apps.especes.tests.factories import EspeceFactory
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestEspeceListView:
    def test_espece_list_view_with_permission(self, client):
        """Teste l'accès à la liste avec les permissions requises."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='view_espece'))
        client.force_login(user)
        EspeceFactory.create_batch(3)
        response = client.get(reverse('especes:espece-list'))
        assert response.status_code == 200
        assert len(response.context['especes']) == 3
        assert 'especes/esp_list.html' in [t.name for t in response.templates]

    def test_espece_list_view_without_permission(self, client):
        """Teste l'accès refusé sans permission."""
        user = UserFactory(is_staff=True)  # Pas de permission
        client.force_login(user)
        response = client.get(reverse('especes:espece-list'))
        assert response.status_code == 403  # Forbidden

    def test_espece_list_view_anonymous(self, client):
        """Teste l'accès refusé pour un utilisateur non connecté."""
        response = client.get(reverse('especes:espece-list'))
        assert response.status_code == 302  # Redirection vers login

@pytest.mark.django_db
class TestEspeceCreateView:
    def test_espece_create_view_with_permission(self, client):
        """Teste la création d'une espèce avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_espece'))
        client.force_login(user)
        response = client.post(reverse('especes:espece-create'), {
            'nom_commun': 'Truite Arc en ciel',
            'nom_scientifique': 'Oncorhynchus mykiss',
            'est_actif': True
        })
        assert response.status_code == 302  # Redirection après succès
        assert Espece.objects.count() == 1
        assert response.url == reverse('especes:espece-list')

    def test_espece_create_view_without_permission(self, client):
        """Teste le refus de création sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        response = client.post(reverse('especes:espece-create'), {
            'nom_commun': 'Espèce Interdite',
            'nom_scientifique': 'Scientifique Interdit',
            'est_actif': True
        })
        assert response.status_code == 403  # Forbidden

    def test_espece_create_view_invalid_data(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_espece'))
        client.force_login(user)
        response = client.post(reverse('especes:espece-create'), {
            'nom_commun': '',  # Champ obligatoire manquant
            'nom_scientifique': 'Oncorhynchus mykiss',
            'est_actif': True
        })
        assert response.status_code == 200
        assert response.context['form'].errors  # Vérifie que des erreurs existent
        assert 'nom_commun' in response.context['form'].errors  # Vérifie que le champ a une erreur

    def test_espece_create_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_espece'))
        client.force_login(user)
        response = client.get(reverse('especes:espece-create'))
        assert response.status_code == 200
        assert 'especes/esp_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestEspeceUpdateView:
    def test_espece_update_view_with_permission(self, client):
        """Teste la mise à jour avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_espece'))
        client.force_login(user)
        espece = EspeceFactory(nom_commun='Ancien Nom')
        response = client.post(reverse('especes:espece-update', args=[espece.id]), {
            'nom_commun': 'Nouveau Nom',
            'nom_scientifique': espece.nom_scientifique,
            'est_actif': False
        })
        assert response.status_code == 302
        espece.refresh_from_db()
        assert espece.nom_commun == 'Nouveau Nom'
        assert espece.est_actif is False

    def test_espece_update_view_without_permission(self, client):
        """Teste le refus de mise à jour sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        espece = EspeceFactory()
        response = client.post(reverse('especes:espece-update', args=[espece.id]), {
            'nom_commun': 'Nom Interdit',
            'nom_scientifique': espece.nom_scientifique,
            'est_actif': espece.est_actif
        })
        assert response.status_code == 403  # Forbidden

    def test_espece_update_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_espece'))
        client.force_login(user)
        espece = EspeceFactory()
        response = client.get(reverse('especes:espece-update', args=[espece.id]))
        assert response.status_code == 200
        assert 'especes/esp_form.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestEspeceDeleteView:
    def test_espece_delete_view_with_permission(self, client):
        """Teste la suppression avec permission."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_espece'))
        client.force_login(user)
        espece = EspeceFactory()
        response = client.post(reverse('especes:espece-delete', args=[espece.id]))
        assert response.status_code == 302
        assert Espece.objects.count() == 0
        assert response.url == reverse('especes:espece-list')

    def test_espece_delete_view_without_permission(self, client):
        """Teste le refus de suppression sans permission."""
        user = UserFactory(is_staff=True)
        client.force_login(user)
        espece = EspeceFactory()
        response = client.post(reverse('especes:espece-delete', args=[espece.id]))
        assert response.status_code == 403  # Forbidden

    def test_espece_delete_view_template(self, client):
        """Teste que le bon template est utilisé."""
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_espece'))
        client.force_login(user)
        espece = EspeceFactory()
        response = client.get(reverse('especes:espece-delete', args=[espece.id]))
        assert response.status_code == 200
        assert 'especes/esp_confirm_delete.html' in [t.name for t in response.templates]
