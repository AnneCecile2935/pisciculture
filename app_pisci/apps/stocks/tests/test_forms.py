import pytest
from apps.stocks.forms import LotForm
from apps.especes.tests.factories import EspeceFactory
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.stocks.tests.factories import LotDePoissonFactory

@pytest.mark.django_db
class TestLotDePoissonForm:
    def test_form_valid(self):
        """Teste un formulaire valide."""
        espece = EspeceFactory()
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        fournisseur = FournisseurFactory()
        form_data = {
            'espece': espece.id,
            'site_prod': site.id,
            'bassin': bassin.id,
            'fournisseur': fournisseur.id,
            'date_arrivee': "2023-01-01",
            'quantite': 1000,
            'statut': 'OEUF',
            'code_lot': 'TESTFORM',
            'poids': 5
        }
        form = LotForm(data=form_data)
        assert form.is_valid()

    def test_form_required_fields(self):
        """Teste que les champs obligatoires sont validés."""
        form = LotForm(data={})
        assert not form.is_valid()
        assert 'espece' in form.errors
        assert 'site_prod' in form.errors
        assert 'bassin' in form.errors
        assert 'fournisseur' in form.errors
        assert 'date_arrivee' in form.errors
        assert 'quantite' in form.errors
        assert 'code_lot' in form.errors
        assert 'poids' in form.errors

    def test_form_unique_code(self):
        """Teste la validation du code unique."""
        espece = EspeceFactory()
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        fournisseur = FournisseurFactory()
        LotDePoissonFactory(code_lot="DUPLICATE", espece=espece, site_prod=site, bassin=bassin, fournisseur=fournisseur)
        form = LotForm(data={
            'espece': espece.id,
            'site_prod': site.id,
            'bassin': bassin.id,
            'fournisseur': fournisseur.id,
            'date_arrivee': "2023-01-01",
            'quantite': 1000,
            'statut': 'OEUF',
            'code_lot': 'DUPLICATE',  # Code dupliqué
            'poids': 5
        })
        assert not form.is_valid()
        assert 'code_lot' in form.errors
