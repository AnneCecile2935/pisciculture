import pytest
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from apps.users.models import User
from apps.stocks.models import LotDePoisson
from apps.especes.tests.factories import EspeceFactory
from apps.sites.tests.factories import BassinFactory, SiteFactory
from apps.fournisseurs.tests.factories import FournisseurFactory


@pytest.mark.django_db  # Active l'accès à la base de données pour tous les tests
class TestLotListView:
    def test_access_for_all_users(self, client, admin_user, standard_user, lot_factory):
        lot = lot_factory()
        # Test avec admin
        client.force_login(admin_user)
        response = client.get(reverse_lazy("stocks:list"))
        assert response.status_code == 200
        assert len(response.context["lots"]) == 1
        # Test avec utilisateur normal
        client.force_login(standard_user)
        response = client.get(reverse_lazy("stocks:list"))
        assert response.status_code == 200
        assert len(response.context["lots"]) == 1

@pytest.mark.django_db
class TestLotCreateView:
    def test_admin_access(self, client, admin_user):
        admin_user.save()  # Force la synchronisation de is_staff
        assert admin_user.is_admin is True
        client.force_login(admin_user)
        response = client.get(reverse_lazy("stocks:create"))
        assert response.status_code == 200

    def test_normal_user_access(self, client, normal_user):
        client.force_login(normal_user)
        response = client.get(reverse_lazy("stocks:create"))
        assert response.status_code == 403
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Vous n'avez pas les droits" in str(messages[0])

    def test_valid_form_submission(self, client, admin_user):
        client.force_login(admin_user)
        espece = EspeceFactory()
        site = SiteFactory()  # ⭐ Crée un site avec une factory
        bassin = BassinFactory(site=site)  # ⭐ Associe le bassin à un site
        fournisseur = FournisseurFactory()  # ⭐ Crée un fournisseur

        form_data = {
            "code_lot": "LOT002",
            "quantite": 2000,
            "poids": 100.0,
            "statut": "OEUF",
            "espece": espece.pk,
            "site_prod": site.pk,  # ⭐ Ajoute le site
            "fournisseur": fournisseur.pk,  # ⭐ Ajoute le fournisseur
            "bassin": bassin.pk,
            "date_arrivee": "2025-10-13",
        }

        response = client.post(reverse_lazy("stocks:create"), data=form_data)
        assert response.status_code == 302  # Doit rediriger
        assert LotDePoisson.objects.filter(code_lot="LOT002").exists()  # Vérifie que le lot est créé

@pytest.mark.django_db
class TestLotUpdateView:
    def test_admin_access(self, client, admin_user, lot_factory):
        lot = lot_factory()
        client.force_login(admin_user)
        response = client.get(reverse_lazy("stocks:update", args=[lot.pk]))
        assert response.status_code == 200

@pytest.mark.django_db
class TestLotDeleteView:
    def test_admin_access(self, client, admin_user, lot_factory):
        lot = lot_factory(code_lot="LOT004")
        client.force_login(admin_user)
        response = client.get(reverse_lazy("stocks:delete", args=[lot.pk]))
        assert response.status_code == 200

@pytest.mark.django_db
class TestGeneralAccess:
    def test_unauthenticated_access_to_all_views(self, client):
        urls = [
            reverse_lazy("stocks:list"),
            reverse_lazy("stocks:create"),
        ]
        for url in urls:
            response = client.get(url)
            assert response.status_code in [302, 403]
