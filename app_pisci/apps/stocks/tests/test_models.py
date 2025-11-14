import pytest
from django.core.exceptions import ValidationError
from apps.stocks.models import LotDePoisson
from apps.stocks.tests.factories import LotDePoissonFactory
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.especes.tests.factories import EspeceFactory
from apps.sites.tests.factories import SiteFactory, BassinFactory

@pytest.mark.django_db
class TestLotDePoissonModel:
    def test_lot_creation(self):
        lot = LotDePoissonFactory()
        assert str(lot) == f"{lot.code_lot} - {lot.espece.nom_commun} (0/{lot.quantite})"
        assert lot.poids_moyen is None  # car quantite_actuelle=0

    def test_lot_poids_moyen_calculation(self):
        lot = LotDePoissonFactory(quantite=2000, poids=4, quantite_actuelle=2000)
        assert lot.poids_moyen == 2.0

    def test_lot_quantite_zero(self):
        lot = LotDePoisson(
            espece=EspeceFactory(),
            site_prod=SiteFactory(),
            fournisseur=FournisseurFactory(),
            date_arrivee="2023-01-01",
            quantite=0,
            statut="OEUF",
            code_lot="TEST001",
            poids=10
        )
        with pytest.raises(ValidationError) as e:
            lot.full_clean()
        assert "La quantité ne peut pas être 0" in str(e.value)

    def test_lot_quantite_positive_constraint(self):
        with pytest.raises(ValidationError):  # Doit lever ValidationError (pas Exception)
            LotDePoissonFactory(quantite=-1)

    def test_lot_unique_code(self):
        LotDePoissonFactory(code_lot="UNIQUE01")
        with pytest.raises(Exception):  # IntegrityError
            LotDePoissonFactory(code_lot="UNIQUE01")

    def test_lot_relations(self):
        espece = EspeceFactory(nom_commun="Truite arc-en-ciel")
        site = SiteFactory(nom="Site Test")
        bassin1 = BassinFactory(site=site, nom="Bassin 1")
        bassin2 = BassinFactory(site=site, nom="Bassin 2")
        fournisseur = FournisseurFactory(nom="Fournisseur Test")

        lot = LotDePoissonFactory(
            espece=espece,
            site_prod=site,
            fournisseur=fournisseur,
            bassins=[bassin1, bassin2]
        )
        assert lot in bassin1.lots_poissons.all()
        assert lot in bassin2.lots_poissons.all()

    def test_lot_ordering(self):
        LotDePoissonFactory(date_arrivee="2023-01-01")
        LotDePoissonFactory(date_arrivee="2023-01-02")
        lots = LotDePoisson.objects.all()
        assert lots[0].date_arrivee > lots[1].date_arrivee

    def test_lot_statut_choices(self):
        lot = LotDePoissonFactory(statut="ALEVIN")
        assert lot.statut in dict(LotDePoisson.STATUT_CHOICES)

    def test_lot_meta_options(self):
        assert LotDePoisson._meta.verbose_name == "Lot de poissons"
        assert LotDePoisson._meta.ordering == ['-date_arrivee']

    def test_lot_unique_per_bassin(self):
        bassin = BassinFactory()
        LotDePoissonFactory(bassins=[bassin])
        with pytest.raises(ValidationError) as e:
            LotDePoissonFactory(bassins=[bassin])
        assert "contient déjà un lot" in str(e.value)
