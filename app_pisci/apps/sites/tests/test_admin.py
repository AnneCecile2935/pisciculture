import pytest
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from apps.sites.models import Site, Bassin
from apps.sites.admin import SiteAdmin, BassinAdmin
from .factories import SiteFactory, BassinFactory

@pytest.mark.django_db
class TestSiteAdmin:
    def test_site_admin(self):
        site_admin = SiteAdmin(Site, AdminSite())
        assert site_admin.list_display == ('nom', 'est_actif', 'created_at')
        assert site_admin.search_fields == ('nom',)

@pytest.mark.django_db
class TestBassinAdmin:
    def test_bassin_admin(self):
        bassin_admin = BassinAdmin(Bassin, AdminSite())
        assert bassin_admin.list_display == ('nom', 'site', 'volume', 'type', 'est_actif', 'created_at')
        assert bassin_admin.list_filter == ('site', 'type', 'est_actif')
        assert bassin_admin.search_fields == ('nom', 'type')
