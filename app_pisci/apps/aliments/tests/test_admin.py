import pytest
from django.contrib.admin.sites import AdminSite
from apps.aliments.admin import AlimentAdmin
from apps.aliments.models import Aliment

@pytest.mark.django_db
class TestAlimentAdmin:
    def test_admin_registration(self):
        from django.contrib import admin
        assert admin.site.is_registered(Aliment)

    def test_admin_config(self):
        admin_site = AdminSite()
        admin_class = AlimentAdmin(Aliment, admin_site)
        assert admin_class.list_display == ("code_alim", "nom", "fournisseur")
