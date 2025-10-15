import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.activite_quotidien.models import Nourrissage
from apps.activite_quotidien.tests.factories import NourrissageFactory
from apps.sites.tests.factories import BassinFactory, SiteFactory
from apps.users.tests.factories import UserFactory
from apps.stocks.tests.factories import LotDePoissonFactory
from apps.aliments.tests.factories import AlimentFactory
from django.utils import timezone

@pytest.mark.django_db
class TestNourrissageModel:
    def test_nourrissage_creation(self):
        """Test : création d'un nourrissage valide."""
        nourrissage = NourrissageFactory()
        assert nourrissage.qte >= 0.01
        assert str(nourrissage) == f"{nourrissage.code_lot} - {nourrissage.qte} kg le {nourrissage.date_repas}"

    def test_nourrissage_qte_minimum(self):
        """Test : la quantité doit être >= 0.01."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin)
        aliment = AlimentFactory()

        nourrissage = Nourrissage(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            aliment=aliment,
            qte=0,  # Quantité invalide
            date_repas='2023-10-15',
            notes='Test note'
        )

        with pytest.raises(ValidationError):
            nourrissage.full_clean()

    def test_nourrissage_str_method(self):
        """Test : la méthode __str__."""
        nourrissage = NourrissageFactory(crea_lot__code_lot="TRUITE-2023")
        assert "TRUITE-2023" in str(nourrissage)

    def test_nourrissage_code_lot_fallback(self):
        """Test : fallback du code_lot si vide."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(bassin=bassin, code_lot="")  # Utilise une chaîne vide
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment)

        assert nourrissage.code_lot == f"LOT-{lot.id}"

    def test_nourrissage_relations(self):
        """Test : les relations ForeignKey sont correctes."""
        nourrissage = NourrissageFactory()
        assert nourrissage.site_prod == nourrissage.bassin.site
        assert nourrissage.crea_lot.bassin == nourrissage.bassin

    def test_nourrissage_cree_par_null(self):
        """Test : cree_par peut être null."""
        nourrissage = NourrissageFactory(cree_par=None)
        assert nourrissage.cree_par is None

    def test_nourrissage_db_table(self):
        """Test : le modèle utilise la bonne table."""
        assert Nourrissage._meta.db_table == 'Repas_journ'

@pytest.mark.django_db
class TestNourrissageValidations:
    def test_qte_min_value(self):
        """Test : la quantité ne peut pas être < 0.01."""
        with pytest.raises(ValidationError) as exc:
            NourrissageFactory(qte=0).full_clean()
        assert "0.01" in str(exc.value)

    def test_date_repas_auto(self):
        """Test : la date est bien enregistrée."""
        nourrissage = NourrissageFactory(date_repas="2023-01-01")
        assert str(nourrissage.date_repas) == "2023-01-01"

    def test_bassin_site_coherence(self):
        """Test : le bassin doit appartenir au site_prod."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        nourrissage = NourrissageFactory(site_prod=site, bassin=bassin)
        assert nourrissage.bassin.site == nourrissage.site_prod

@pytest.mark.django_db
class TestNourrissageRelations:
    def test_nourrissage_lot_relation(self):
        """Test : un nourrissage est lié à un lot de poissons."""
        lot = LotDePoissonFactory()
        nourrissage = NourrissageFactory(crea_lot=lot)
        assert nourrissage in lot.nourrissages.all()

    def test_nourrissage_user_relation(self):
        """Test : la relation avec l'utilisateur (cree_par)."""
        user = UserFactory()
        nourrissage = NourrissageFactory(cree_par=user)
        assert nourrissage.cree_par == user

    def test_delete_lot_deletes_nourrissages(self):
        """Test : supprimer un lot supprime ses nourrissages."""
        lot = LotDePoissonFactory()
        NourrissageFactory(crea_lot=lot)
        assert lot.nourrissages.count() == 1
        lot.delete()
        assert Nourrissage.objects.count() == 0

    def test_delete_user_does_not_delete_nourrissage(self):
        """Test : supprimer un utilisateur ne supprime pas les nourrissages."""
        user = UserFactory()
        nourrissage = NourrissageFactory(cree_par=user)
        user.delete()
        assert Nourrissage.objects.filter(id=nourrissage.id).exists()
        assert Nourrissage.objects.get(id=nourrissage.id).cree_par is None

@pytest.mark.django_db
class TestNourrissageQueries:
    def test_filter_by_site(self):
        """Test : filtrer les nourrissages par site."""
        site1 = SiteFactory()
        site2 = SiteFactory()
        NourrissageFactory(site_prod=site1)
        NourrissageFactory(site_prod=site2)
        assert Nourrissage.objects.filter(site_prod=site1).count() == 1

    def test_filter_by_date(self):
        """Test : filtrer les nourrissages par date."""
        date = timezone.now().date()
        NourrissageFactory(date_repas=date)
        NourrissageFactory(date_repas=timezone.now().date() - timezone.timedelta(days=1))
        assert Nourrissage.objects.filter(date_repas=date).count() == 1

    def test_order_by_date(self):
        """Test : trier les nourrissages par date."""
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        NourrissageFactory(date_repas=yesterday)
        NourrissageFactory(date_repas=timezone.now().date())
        nourrissages = Nourrissage.objects.order_by('date_repas')
        assert nourrissages[0].date_repas == yesterday
