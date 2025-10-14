import pytest
from django.contrib.admin.sites import AdminSite
from apps.stocks.admin import LotDePoissonAdmin
from apps.stocks.models import LotDePoisson

@pytest.mark.django_db
class TestLotDePoissonAdmin:
    def test_admin_registration(self):
        from django.contrib import admin
        assert admin.site.is_registered(LotDePoisson)

    def test_admin_config(self):
        admin_site = AdminSite()
        admin_class = LotDePoissonAdmin(LotDePoisson, admin_site)
        assert admin_class.list_display == ('code_lot', 'espece', 'site_prod', 'bassin', 'date_arrivee', 'quantite', 'statut')
        assert admin_class.list_filter == ('site_prod', 'espece', 'statut')
