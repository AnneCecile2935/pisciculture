import pytest
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.test import Client
from apps.fournisseurs.models import Fournisseur
from apps.fournisseurs.admin import FournisseurAdmin
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestFournisseurAdmin:
    def test_fournisseur_admin_registration(self):
        """Teste que le modèle Fournisseur est bien enregistré dans l'admin."""
        assert admin.site.is_registered(Fournisseur)

    def test_fournisseur_admin_config(self):
        """Teste la configuration de FournisseurAdmin."""
        admin_site = AdminSite()
        admin_class = FournisseurAdmin(Fournisseur, admin_site)

        # Vérifie list_display
        assert admin_class.list_display == ('nom', 'ville', 'get_type_fournisseur_display', 'est_actif')

        # Vérifie list_filter
        assert admin_class.list_filter == ('type_fournisseur', 'est_actif')

        # Vérifie search_fields
        assert admin_class.search_fields == ('nom', 'ville', 'contact')

    def test_fournisseur_admin_list_display(self, client):
        """Teste l'affichage de la liste dans l'admin."""
        # Crée un utilisateur admin
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Crée un fournisseur de test
        Fournisseur.objects.create(
            nom="Test Admin",
            adresse="123 Rue Test",
            ville="Testville",
            code_postal="35000",
            type_fournisseur="ALIMENT",
            est_actif=True
        )

        # Accède à la page de liste de l'admin
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'))
        assert response.status_code == 200
        assert b"Test Admin" in response.content
        assert b"Testville" in response.content
        assert b"Aliment" in response.content  # get_type_fournisseur_display

    def test_fournisseur_admin_search(self, client):
        """Teste la fonctionnalité de recherche dans l'admin."""
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Crée un fournisseur pour la recherche
        Fournisseur.objects.create(
            nom="Fournisseur Recherche",
            adresse="456 Rue Recherche",
            ville="Rechercheville",
            code_postal="75000",
            type_fournisseur="OEUFS",
            contact="Contact Recherche",
            est_actif=True
        )

        # Effectue une recherche par nom
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'), {'q': 'Recherche'})
        assert response.status_code == 200
        assert b"Fournisseur Recherche" in response.content

        # Effectue une recherche par ville
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'), {'q': 'Rechercheville'})
        assert response.status_code == 200
        assert b"Fournisseur Recherche" in response.content

        # Effectue une recherche par contact
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'), {'q': 'Contact Recherche'})
        assert response.status_code == 200
        assert b"Fournisseur Recherche" in response.content

    def test_fournisseur_admin_filters(self, client):
        """Teste les filtres dans l'admin."""
        user = UserFactory(is_staff=True, is_superuser=True)
        client.force_login(user)

        # Utilise la factory pour créer des fournisseurs valides
        FournisseurFactory(nom="Fournisseur Aliment", ville="Ville Aliment", type_fournisseur="ALIMENT", est_actif=True)
        FournisseurFactory(nom="Fournisseur Oeufs", ville="Ville Oeufs", type_fournisseur="OEUFS", est_actif=False)

        # Filtre par type_fournisseur=ALIMENT
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'), {'type_fournisseur': 'ALIMENT'})
        assert response.status_code == 200
        assert b"Fournisseur Aliment" in response.content
        assert b"Fournisseur Oeufs" not in response.content

        # Filtre par est_actif=True
        response = client.get(reverse('admin:fournisseurs_fournisseur_changelist'), {'est_actif': '1'})
        assert response.status_code == 200
        assert b"Fournisseur Aliment" in response.content
        assert b"Fournisseur Oeufs" not in response.content
