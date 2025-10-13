import pytest
from django import forms
from apps.sites.forms import SiteForm, BassinForm
from apps.sites.tests.factories import SiteFactory

@pytest.mark.django_db
class TestSiteForm:
    def test_site_form_valid(self):
        form = SiteForm(data={'nom': 'Nouveau Site', 'est_actif': True})
        assert form.is_valid()

    def test_site_form_invalid(self):
        form = SiteForm(data={'nom': '', 'est_actif': True})
        assert not form.is_valid()
        assert 'nom' in form.errors

@pytest.mark.django_db
class TestBassinForm:
    def test_bassin_form_valid(self):
        site = SiteFactory()
        form = BassinForm(data={
            'nom': 'Nouveau Bassin',
            'site': site.id,
            'volume': 100.5,
            'type': 'Écloserie',
            'est_actif': True
        })
        assert form.is_valid()

    def test_bassin_form_invalid(self):
        form = BassinForm(data={  # ← Assure-toi que 'form' est bien défini ici
            'nom': '',
            'site': '',
            'volume': -10,
            'type': 'x' * 101,
            'est_actif': True
        })
        assert not form.is_valid()
        assert 'nom' in form.errors
        assert 'site' in form.errors
        assert 'volume' in form.errors
        assert 'type' in form.errors
