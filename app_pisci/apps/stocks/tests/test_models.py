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
        """Teste la création d'un lot avec des données valides."""
        lot = LotDePoissonFactory(
            code_lot="TEST001",
            quantite=5000,
            poids=10
        )
        assert str(lot) == f"TEST001 - {lot.espece.nom_commun} (5000/5000)"
        assert lot.poids_moyen == 2.0  # 10kg * 1000 / 5000 = 2g

    def test_lot_poids_moyen_calculation(self):
        """Teste le calcul automatique du poids moyen."""
        lot = LotDePoissonFactory(quantite=2000, poids=4)
        assert lot.poids_moyen == 2.0  # 4kg * 1000 / 2000 = 2g

    def test_lot_quantite_zero(self):
        """Teste que quantite=0 lève une ValidationError (avant la contrainte DB)."""
        lot = LotDePoisson(
            espece=EspeceFactory(),
            site_prod=SiteFactory(),
            bassin=BassinFactory(),
            fournisseur=FournisseurFactory(),
            date_arrivee="2023-01-01",
            quantite=0,  # ← Quantité invalide
            statut="OEUF",
            code_lot="TEST001",
            poids=10
        )
        with pytest.raises(ValidationError) as e:  # Doit lever ValidationError, pas IntegrityError
            lot.full_clean()  # ← Appelle clean() et valide les contraintes
        assert "La quantité ne peut pas être 0" in str(e.value)

    def test_lot_quantite_positive_constraint(self):
        """Teste la contrainte quantite_positive."""
        with pytest.raises(Exception):  # Violation de contrainte DB
            LotDePoissonFactory(quantite=-1)

    def test_lot_unique_code(self):
        """Teste que code_lot est unique."""
        LotDePoissonFactory(code_lot="UNIQUE01")
        with pytest.raises(Exception):  # Violation d'unicité
            LotDePoissonFactory(code_lot="UNIQUE01")

    def test_lot_relations(self):
        """Teste les relations avec Espece, Site, Bassin et Fournisseur."""
        espece = EspeceFactory(nom_commun="Truite arc-en-ciel")
        site = SiteFactory(nom="Site Test")
        bassin = BassinFactory(site=site, nom="Bassin 1")
        fournisseur = FournisseurFactory(nom="Fournisseur Test")
        lot = LotDePoissonFactory(
            espece=espece,
            site_prod=site,
            bassin=bassin,
            fournisseur=fournisseur
        )
        assert lot in espece.lots.all()
        assert lot in site.lots_poissons.all()
        assert lot in bassin.lots_poissons.all()
        assert lot in fournisseur.lot_fournis.all()

    def test_lot_ordering(self):
        """Teste le tri par date_arrivee (décroissant)."""
        LotDePoissonFactory(date_arrivee="2023-01-01")
        LotDePoissonFactory(date_arrivee="2023-01-02")
        lots = LotDePoisson.objects.all()
        assert lots[0].date_arrivee > lots[1].date_arrivee

    def test_lot_statut_choices(self):
        """Teste que statut est limité aux choix définis."""
        lot = LotDePoissonFactory(statut="ALEVIN")
        assert lot.statut in dict(LotDePoisson.STATUT_CHOICES)

    def test_lot_meta_options(self):
        """Teste les options Meta du modèle."""
        assert LotDePoisson._meta.verbose_name == "Lot de poissons"
        assert LotDePoisson._meta.verbose_name_plural == "Lots de poissons"
        assert LotDePoisson._meta.ordering == ['-date_arrivee']
