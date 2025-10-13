import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from apps.sites.models import Site, Bassin
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.users.tests.factories import UserFactory

@pytest.mark.django_db
class TestSiteViews:
    def test_site_list_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='view_site'))
        client.force_login(user)
        SiteFactory.create_batch(3)
        response = client.get(reverse('sites:site-list'))
        assert response.status_code == 200
        assert len(response.context['sites']) == 3

    def test_site_create_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_site'))
        client.force_login(user)
        response = client.post(reverse('sites:site-create'), {
            'nom': 'Nouveau Site',
            'est_actif': True
        })
        assert response.status_code == 302
        assert Site.objects.count() == 1

    def test_site_update_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_site'))
        client.force_login(user)
        site = SiteFactory(nom='Site à modifier')
        response = client.post(reverse('sites:site-update', args=[site.id]), {
            'nom': 'Site modifié',
            'est_actif': False
        })
        assert response.status_code == 302
        site.refresh_from_db()
        assert site.nom == 'Site modifié'
        assert site.est_actif is False

    def test_site_delete_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_site'))
        client.force_login(user)
        site = SiteFactory()
        response = client.post(reverse('sites:site-delete', args=[site.id]))
        assert response.status_code == 302
        assert Site.objects.count() == 0

@pytest.mark.django_db
class TestBassinViews:
    def test_bassin_list_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='view_bassin'))
        client.force_login(user)
        site = SiteFactory()
        BassinFactory.create_batch(2, site=site)
        response = client.get(reverse('sites:bassin-list', args=[site.id]))
        assert response.status_code == 200
        assert len(response.context['bassins']) == 2

    def test_bassin_create_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='add_bassin'))
        client.force_login(user)
        site = SiteFactory()
        response = client.post(reverse('sites:bassin-create'), {
            'nom': 'Nouveau Bassin',
            'site': site.id,
            'volume': 100.5,
            'type': 'Écloserie',
            'est_actif': True
        })
        assert response.status_code == 302
        assert Bassin.objects.count() == 1

    def test_bassin_update_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='change_bassin'))
        client.force_login(user)
        bassin = BassinFactory(nom='Bassin à modifier', volume=100.0)
        response = client.post(reverse('sites:bassin-update', args=[bassin.id]), {
            'nom': 'Bassin modifié',
            'site': bassin.site.id,
            'volume': 200.0,
            'type': 'Grossissement',
            'est_actif': False
        })
        assert response.status_code == 302
        bassin.refresh_from_db()
        print(bassin.volume)  # ← Affiche la valeur réelle pour déboguer
        assert bassin.nom == 'Bassin modifié'
        assert bassin.volume == 200.0  # Doit maintenant fonctionner

    def test_bassin_delete_view(self, client):
        user = UserFactory(is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename='delete_bassin'))
        client.force_login(user)
        bassin = BassinFactory()
        response = client.post(reverse('sites:bassin-delete', args=[bassin.id]))
        assert response.status_code == 302
        # Vérifie que la redirection utilise le bon nom d'URL :
        assert response.url == reverse('sites:site-list')  # ← `bassin-list` avec tiret
        assert Bassin.objects.count() == 0
