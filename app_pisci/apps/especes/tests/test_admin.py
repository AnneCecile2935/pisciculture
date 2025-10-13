import pytest
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.test import Client
from apps.especes.models import Espece
from apps.especes.admin import EspeceAdmin
from apps.users.tests.factories import UserFactory
from apps.especes.tests.factories import EspeceFactory

@pytest.mark.django_db
class TestEspeceAdmin:
    def test_espece_admin_registration(self):
        """Teste que le modèle Espece est bien enregistré dans l'admin."""
        from django.contrib import admin
        assert admin.site.is_registered(Espece)

    def test_espece_admin_config(self):
        """Teste la configuration de EspeceAdmin."""
        admin_site = AdminSite()
        admin_class = EspeceAdmin(Espece, admin_site)

        # Vérifie list_display
        assert admin_class.list_display == ('nom_commun', 'nom_scientifique', 'est_actif')

        # Vérifie list_filter
        assert admin_class.list_filter == ('est_actif',)

        # Vérifie search_fields
        assert admin_class.search_fields == ('nom_commun', 'nom_scientifique')

    def test_espece_admin_list_display(self, client):
        """Teste l'affichage de la liste dans l'admin."""
        # Crée un utilisateur admin
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Crée une espèce de test
        EspeceFactory(nom_commun="Truite Arc en ciel", nom_scientifique="Oncorhynchus mykiss")

        # Accède à la page de liste de l'admin
        response = client.get(reverse('admin:especes_espece_changelist'))
        assert response.status_code == 200
        assert "Truite Arc en ciel".encode() in response.content
        assert "Oncorhynchus mykiss".encode() in response.content

    def test_espece_admin_search(self, client):
        """Teste la fonctionnalité de recherche dans l'admin."""
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Crée une espèce pour la recherche
        EspeceFactory(nom_commun="Espece Recherche", nom_scientifique="Scientifique Recherche")

        # Effectue une recherche par nom_commun
        response = client.get(reverse('admin:especes_espece_changelist'), {'q': 'Recherche'})
        assert response.status_code == 200
        assert "Espece Recherche".encode() in response.content

        # Effectue une recherche par nom_scientifique
        response = client.get(reverse('admin:especes_espece_changelist'), {'q': 'Scientifique Recherche'})
        assert response.status_code == 200
        assert "Espece Recherche".encode() in response.content

    def test_espece_admin_filters(self, client):
        """Teste les filtres dans l'admin."""
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Crée des espèces avec différents statuts
        EspeceFactory(nom_commun="Espece Active", est_actif=True)
        EspeceFactory(nom_commun="Espece Inactive", est_actif=False)

        # Filtre par est_actif=True
        response = client.get(reverse('admin:especes_espece_changelist'), {'est_actif': '1'})
        assert response.status_code == 200
        assert "Espece Active".encode() in response.content
        assert "Espece Inactive".encode() not in response.content

        # Filtre par est_actif=False
        response = client.get(reverse('admin:especes_espece_changelist'), {'est_actif': '0'})
        assert response.status_code == 200
        assert "Espece Inactive".encode() in response.content
        assert "Espece Active".encode() not in response.content
