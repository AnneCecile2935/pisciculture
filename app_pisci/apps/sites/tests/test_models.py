import pytest
from django.core.exceptions import ValidationError
from apps.sites.models import Site, Bassin
from .factories import SiteFactory, BassinFactory

@pytest.mark.django_db
class TestSiteModel:
    def test_site_creation(self):
        site = SiteFactory(nom="Site Test")
        assert str(site) == "Site Test"
        assert site.est_actif is True

    def test_site_unique_nom(self):
        SiteFactory(nom="Unique Site")
        with pytest.raises(ValidationError):  # IntegrityError
            site = Site(nom="Unique Site")
            site.full_clean()

@pytest.mark.django_db
class TestBassinModel:
    def test_bassin_creation(self):
        site = SiteFactory(nom="Site Test")
        bassin = BassinFactory(site=site, nom="Bassin Test")
        assert str(bassin) == "Bassin Test (Site Test)"
        assert bassin.volume is not None

    def test_bassin_unique_together(self):
        site = SiteFactory(nom="Site Test")
        BassinFactory(site=site, nom="Unique Bassin")
        with pytest.raises(ValidationError):
            bassin = Bassin(site=site, nom="Unique Bassin")  # Objet non sauvegardé
            bassin.full_clean()  # Déclenche la validation
            
    def test_bassin_ordering(self):
        site = SiteFactory()
        BassinFactory(site=site, nom="Bassin B")
        BassinFactory(site=site, nom="Bassin A")
        bassins = Bassin.objects.all()
        assert bassins[0].nom == "Bassin A"
        assert bassins[1].nom == "Bassin B"
