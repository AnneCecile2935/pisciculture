import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.stocks.tests.factories import LotDePoissonFactory
from apps.activite_quotidien.tests.factories import NourrissageFactory
from apps.aliments.tests.factories import AlimentFactory
from apps.activite_quotidien.models import Nourrissage

@pytest.mark.django_db
class TestNourrissageCreateView:
    def test_create_nourrissage_success(self, client, standard_user):
        """Test : création réussie d'un repas."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()

        data = {
            'site_prod': site.id,
            'bassin': bassin.id,
            'crea_lot': lot.id,
            'aliment': aliment.id,
            'qte': 2.5,
            'date_repas': '2023-10-15',
            'notes': 'Test note'
        }
        response = client.post(reverse('activite_quotidien:nourrissage-create'), data, follow=True)

        assert response.status_code == 200
        assert Nourrissage.objects.count() == 1
        assert Nourrissage.objects.first().cree_par == standard_user
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le repas a été enregistré avec succès!" in str(messages[0])

    def test_create_nourrissage_invalid_bassin_site(self, client, standard_user):
        """Test : échec si le bassin n'appartient pas au site."""
        client.force_login(standard_user)
        site1 = SiteFactory()
        site2 = SiteFactory()
        bassin = BassinFactory(site=site2)  # Bassin d'un autre site
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()

        data = {
            'site_prod': site1.id,
            'bassin': bassin.id,
            'crea_lot': lot.id,
            'aliment': aliment.id,
            'qte': 2.5,
            'date_repas': '2023-10-15',
            'notes': 'Test note'
        }
        response = client.post(reverse('activite_quotidien:nourrissage-create'), data, follow=True)

        assert response.status_code == 200
        assert Nourrissage.objects.count() == 0
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le bassin ne appartient pas au site sélectionné" in str(messages[0])

    def test_create_nourrissage_invalid_lot_bassin(self, client, standard_user):
        """Test : échec si le lot n'appartient pas au bassin."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin1 = BassinFactory(site=site)
        bassin2 = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin2)  # Lot d'un autre bassin
        aliment = AlimentFactory()

        data = {
            'site_prod': site.id,
            'bassin': bassin1.id,
            'crea_lot': lot.id,
            'aliment': aliment.id,
            'qte': 2.5,
            'date_repas': '2023-10-15',
            'notes': 'Test note'
        }
        response = client.post(reverse('activite_quotidien:nourrissage-create'), data, follow=True)

        assert response.status_code == 200
        assert Nourrissage.objects.count() == 0
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le lot ne appartient pas au bassin sélectionné" in str(messages[0])

    def test_create_nourrissage_unauthenticated(self, client):
        """Test : accès refusé si non authentifié."""
        response = client.get(reverse('activite_quotidien:nourrissage-create'))
        assert response.status_code == 302  # Redirection vers login
        assert response.url.startswith('/login/')

@pytest.mark.django_db
class TestNourrissageListView:
    def test_list_nourrissage(self, client, standard_user):
        """Test : affichage de la liste des repas."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment, cree_par=standard_user)

        response = client.get(reverse('activite_quotidien:nourrissage-list'))
        assert response.status_code == 200
        assert len(response.context['nourrissages']) == 1

    def test_list_nourrissage_unauthenticated(self, client):
        """Test : accès refusé si non authentifié."""
        response = client.get(reverse('activite_quotidien:nourrissage-list'))
        assert response.status_code == 302
        assert response.url.startswith('/login/')

@pytest.mark.django_db
class TestNourrissageDetailView:
    def test_detail_nourrissage(self, client, standard_user):
        """Test : affichage des détails d'un repas."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment, cree_par=standard_user)

        response = client.get(reverse('activite_quotidien:nourrissage-detail', args=[nourrissage.id]))
        assert response.status_code == 200
        assert response.context['nourrissage'] == nourrissage

    def test_detail_nourrissage_unauthenticated(self, client):
        """Test : accès refusé si non authentifié."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment)

        response = client.get(reverse('activite_quotidien:nourrissage-detail', args=[nourrissage.id]))
        assert response.status_code == 302
        assert response.url.startswith('/login/')

@pytest.mark.django_db
class TestNourrissageUpdateView:
    def test_update_nourrissage_success(self, client, standard_user):
        """Test : mise à jour réussie d'un repas."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment, cree_par=standard_user)

        data = {
            'site_prod': site.id,
            'bassin': bassin.id,
            'crea_lot': lot.id,
            'aliment': aliment.id,
            'qte': 3.0,  # Nouvelle quantité
            'date_repas': '2023-10-16',
            'notes': 'Updated note'
        }
        response = client.post(reverse('activite_quotidien:nourrissage-update', args=[nourrissage.id]), data, follow=True)

        assert response.status_code == 200
        nourrissage.refresh_from_db()
        assert nourrissage.qte == 3.0
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le repas a été mis à jour avec succès!" in str(messages[0])

    def test_update_nourrissage_invalid_bassin_site(self, client, standard_user):
        """Test : échec si le bassin n'appartient pas au site après mise à jour."""
        client.force_login(standard_user)
        site1 = SiteFactory()
        site2 = SiteFactory()
        bassin1 = BassinFactory(site=site1)
        bassin2 = BassinFactory(site=site2)
        lot = LotDePoissonFactory(bassin=bassin1)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin1, site_prod=site1, aliment=aliment, cree_par=standard_user)

        data = {
            'site_prod': site1.id,
            'bassin': bassin2.id,  # Bassin d'un autre site
            'crea_lot': lot.id,
            'aliment': aliment.id,
            'qte': 3.0,
            'date_repas': '2023-10-16',
            'notes': 'Updated note'
        }
        response = client.post(reverse('activite_quotidien:nourrissage-update', args=[nourrissage.id]), data, follow=True)

        assert response.status_code == 200
        nourrissage.refresh_from_db()
        assert nourrissage.bassin == bassin1  # Pas de changement
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le bassin ne appartient pas au site sélectionné" in str(messages[0])

    def test_update_nourrissage_unauthenticated(self, client):
        """Test : accès refusé si non authentifié."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment)

        response = client.get(reverse('activite_quotidien:nourrissage-update', args=[nourrissage.id]))
        assert response.status_code == 302
        assert response.url.startswith('/login/')

@pytest.mark.django_db
class TestNourrissageDeleteView:
    def test_delete_nourrissage_success(self, client, standard_user):
        """Test : suppression réussie d'un repas."""
        client.force_login(standard_user)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment, cree_par=standard_user)

        response = client.post(reverse('activite_quotidien:nourrissage-delete', args=[nourrissage.id]), follow=True)
        assert response.status_code == 200
        assert Nourrissage.objects.count() == 0
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert "Le repas a bien été supprimé" in str(messages[0])

    def test_delete_nourrissage_unauthenticated(self, client):
        """Test : accès refusé si non authentifié."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment)

        response = client.get(reverse('activite_quotidien:nourrissage-delete', args=[nourrissage.id]))
        assert response.status_code == 302
        assert response.url.startswith('/login/')
