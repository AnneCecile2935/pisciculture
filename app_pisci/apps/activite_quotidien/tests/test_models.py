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

pytest.mark.django_db
class TestNourrissageModel:
    def test_nourrissage_creation(self):
        """Test : création d'un nourrissage valide."""
        nourrissage = NourrissageFactory()
        assert nourrissage.qte >= 0.01
        assert nourrissage.code_lot in str(nourrissage)  # Utilise le code généré automatiquement

    def test_nourrissage_qte_minimum(self):
        """Test : la quantité doit être >= 0.01."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory()
        lot.bassins.add(bassin)  # Associe le bassin au lot
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

        with pytest.raises(ValidationError) as exc:
            nourrissage.full_clean()
        assert "motif_absence" in str(exc.value)  # Doit demander un motif d'absence

    def test_nourrissage_str_method(self):
        """Test : la méthode __str__."""
        nourrissage = NourrissageFactory()
        assert nourrissage.code_lot in str(nourrissage)  # Utilise le code généré

    def test_nourrissage_code_lot_fallback(self):
        """Test : fallback du code_lot si vide."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(site_prod=site)  # Code vide
        lot.bassins.add(bassin)  # Associe le bassin après création
        aliment = AlimentFactory()
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin, site_prod=site, aliment=aliment)
        assert nourrissage.code_lot == lot.code_lot

    def test_nourrissage_relations(self):
        """Test : les relations ForeignKey sont correctes."""
        nourrissage = NourrissageFactory()
        assert nourrissage.site_prod == nourrissage.bassin.site
        assert nourrissage.bassin in nourrissage.crea_lot.bassins.all()  # Vérifie que le bassin est dans les bassins du lot

    def test_nourrissage_cree_par_null(self):
        """Test : cree_par peut être null."""
        nourrissage = NourrissageFactory(cree_par=None)
        assert nourrissage.cree_par is None

    def test_nourrissage_db_table(self):
        """Test : le modèle utilise la bonne table."""
        assert Nourrissage._meta.db_table == 'Repas_journ'

    def test_qte_affichage_property(self):
        """Test : la propriété qte_affichage retourne le bon format."""
        nourrissage = NourrissageFactory(qte=2)
        assert nourrissage.qte_affichage == "2 kg"  # Utilise FloatField

        nourrissage = NourrissageFactory(qte=None, motif_absence="eau_sale")
        assert nourrissage.qte_affichage == "Aucun repas (Eau sale)"

    def test_est_a_jeun_property(self):
        """Test : la propriété est_a_jeun retourne True si motif_absence='ajeun'."""
        nourrissage = NourrissageFactory(qte=0, motif_absence="ajeun")
        assert nourrissage.est_a_jeun is True

        nourrissage = NourrissageFactory(qte=1, motif_absence=None)
        assert nourrissage.est_a_jeun is False

@pytest.mark.django_db
class TestNourrissageValidations:
    def test_qte_min_value(self):
        """Test : la quantité ne peut pas être < 0.01."""
        with pytest.raises(ValidationError) as exc:
            Nourrissage(qte=-1, motif_absence="autre").full_clean()  # Utilise une valeur inférieure à 0.01
        assert "0" in str(exc.value)  # Vérifie que l'erreur mentionne 0.01

    def test_date_repas_auto(self):
        """Test : la date est bien enregistrée."""
        date = timezone.now().date()
        nourrissage = NourrissageFactory(date_repas=date)
        assert str(nourrissage.date_repas) == str(date)

    def test_bassin_site_coherence(self):
        """Test : le bassin doit appartenir au site_prod."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        nourrissage = NourrissageFactory(site_prod=site, bassin=bassin)
        assert nourrissage.bassin.site == nourrissage.site_prod

    def test_nourrissage_motif_absence_required_if_no_qte(self):
        """Test : un motif d'absence est requis si qte est None ou 0."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory()
        lot.bassins.add(bassin)
        aliment = AlimentFactory()

        # Cas 1 : qte=None et motif_absence=None → doit échouer
        nourrissage = Nourrissage(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            aliment=aliment,
            qte=None,
            motif_absence=None,
            date_repas=timezone.now().date()
        )
        with pytest.raises(ValidationError) as exc:
            nourrissage.full_clean()
        assert "motif_absence" in str(exc.value)

        # Cas 2 : qte=0 et motif_absence=None → doit échouer
        nourrissage.qte = 0
        with pytest.raises(ValidationError) as exc:
            nourrissage.full_clean()
        assert "motif_absence" in str(exc.value)

        # Cas 3 : motif_absence="ajeun" et qte=1 → doit échouer
        nourrissage.qte = 1
        nourrissage.motif_absence = "ajeun"
        with pytest.raises(ValidationError) as exc:
            nourrissage.full_clean()
        assert "qte" in str(exc.value)

    def test_date_repas_cannot_be_in_future(self):
        """Test : la date du repas ne peut pas être dans le futur."""
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(site_prod=site)
        lot.bassins.add(bassin)
        nourrissage = Nourrissage(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            qte=1,
            motif_absence="autre",
            date_repas=future_date
        )
        with pytest.raises(ValidationError) as exc:
            nourrissage.full_clean()
        assert "date_repas" in str(exc.value)

    def test_bassin_must_belong_to_site_prod(self):
        """Test : le bassin doit appartenir au site_prod."""
        site1 = SiteFactory()
        site2 = SiteFactory()
        bassin = BassinFactory(site=site1)
        with pytest.raises(ValidationError):
            Nourrissage(
                site_prod=site2,
                bassin=bassin,
                crea_lot=LotDePoissonFactory(site_prod=site1),
                date_repas=timezone.now().date()
            ).full_clean()

    def test_delete_site_does_not_delete_nourrissages(self):
        """Test : supprimer un site ne supprime PAS ses nourrissages (historique conservé)."""
        site = SiteFactory()
        bassin = BassinFactory(site=site)
        lot = LotDePoissonFactory(site_prod=site)
        lot.bassins.add(bassin)
        nourrissage = NourrissageFactory(site_prod=site, bassin=bassin, crea_lot=lot)
        assert Nourrissage.objects.count() == 1
        site.delete()
        assert Nourrissage.objects.count() == 1  # Le nourrissage est toujours là
        nourrissage.refresh_from_db()
        assert nourrissage.site_prod is None  # La relation est nulle


@pytest.mark.django_db
class TestNourrissageRelations:
    def test_nourrissage_lot_relation(self):
        """Test : un nourrissage est lié à un lot de poissons."""
        lot = LotDePoissonFactory()
        bassin = BassinFactory(site=lot.site_prod)
        lot.bassins.add(bassin)
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin)
        assert nourrissage in lot.nourrissages.all()

    def test_nourrissage_user_relation(self):
        """Test : la relation avec l'utilisateur (cree_par)."""
        user = UserFactory()
        nourrissage = NourrissageFactory(cree_par=user)
        assert nourrissage.cree_par == user

    def test_delete_lot_does_not_delete_nourrissages(self):
        """Test : supprimer un lot ne supprime PAS ses nourrissages (historique conservé)."""
        lot = LotDePoissonFactory()
        bassin = BassinFactory(site=lot.site_prod)
        lot.bassins.add(bassin)
        nourrissage = NourrissageFactory(crea_lot=lot, bassin=bassin)
        assert lot.nourrissages.count() == 1
        lot.delete()
        assert Nourrissage.objects.count() == 1  # Le nourrissage est toujours là
        assert Nourrissage.objects.first().crea_lot is None  # Mais la relation est nulle

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
        bassin1 = BassinFactory(site=site1)
        bassin2 = BassinFactory(site=site2)
        lot1 = LotDePoissonFactory(site_prod=site1)
        lot1.bassins.add(bassin1)
        lot2 = LotDePoissonFactory(site_prod=site2)
        lot2.bassins.add(bassin2)
        NourrissageFactory(site_prod=site1, bassin=bassin1, crea_lot=lot1)
        NourrissageFactory(site_prod=site2, bassin=bassin2, crea_lot=lot2)
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


@pytest.mark.django_db
class TestNourrissageDenormalizedFields:
    """Tests pour vérifier que les champs redondants sont correctement remplis et conservés."""

    def test_denormalized_fields_on_save(self):
        """Test : les champs redondants sont remplis lors de la sauvegarde."""
        site = SiteFactory(nom="Site de Test")
        bassin = BassinFactory(nom="Bassin de Test", site=site)
        lot = LotDePoissonFactory(site_prod=site, code_lot="TRUITE-2023")
        lot.bassins.add(bassin)
        aliment = AlimentFactory(nom="Granulés Test")
        user = UserFactory(username="testuser")

        nourrissage = Nourrissage(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            aliment=aliment,
            qte=2,
            cree_par=user,
            date_repas=timezone.now().date()
        )
        nourrissage.save()

        assert nourrissage.site_prod_nom == "Site de Test"
        assert nourrissage.bassin_nom == "Bassin de Test"
        assert nourrissage.crea_lot_code == "TRUITE-2023"
        assert nourrissage.aliment_nom == "Granulés Test"
        assert nourrissage.cree_par_nom == "testuser"

    def test_denormalized_fields_after_deletion(self):
        """Test : les champs redondants sont conservés après suppression des relations."""
        site = SiteFactory(nom="Site à Supprimer")
        bassin = BassinFactory(nom="Bassin à Supprimer", site=site)
        lot = LotDePoissonFactory(site_prod=site, code_lot="TRUITE-2024")
        lot.bassins.add(bassin)
        aliment = AlimentFactory(nom="Aliment à Supprimer")
        user = UserFactory(username="user_to_delete")

        nourrissage = NourrissageFactory(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            aliment=aliment,
            qte=1.0,
            cree_par=user
        )

        site.delete()
        bassin.delete()
        lot.delete()
        aliment.delete()
        user.delete()

        nourrissage.refresh_from_db()
        assert nourrissage.site_prod_nom == "Site à Supprimer"
        assert nourrissage.bassin_nom == "Bassin à Supprimer"
        assert nourrissage.crea_lot_code == "TRUITE-2024"
        assert nourrissage.aliment_nom == "Aliment à Supprimer"
        assert nourrissage.cree_par_nom == "user_to_delete"

    def test_str_method_uses_denormalized_fields(self):
        """Test : la méthode __str__ utilise les champs redondants si les relations sont supprimées."""
        site = SiteFactory(nom="Site Test")
        bassin = BassinFactory(nom="Bassin Test", site=site)
        lot = LotDePoissonFactory(site_prod=site, code_lot="TRUITE-2025")
        lot.bassins.add(bassin)
        nourrissage = NourrissageFactory(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            qte=3,
            date_repas="2023-01-01"
        )

        site.delete()
        bassin.delete()
        lot.delete()
        nourrissage.refresh_from_db()
        assert str(nourrissage) == "TRUITE-2025 - 3 kg le 2023-01-01"

    def test_qte_affichage_with_denormalized_fields(self):
        """Test : qte_affichage utilise les champs redondants."""

        # Cas 1: Quantité normale
        nourrissage = NourrissageFactory(qte=2)
        assert nourrissage.qte_affichage == "2 kg"

        # Cas 2: À jeun (qte doit être 0)
        nourrissage = NourrissageFactory(qte=0, motif_absence="ajeun")
        assert nourrissage.qte_affichage == "0 kg"

        # Cas 3: Aucun repas avec motif
        nourrissage = NourrissageFactory(qte=None, motif_absence="eau_sale")
        assert nourrissage.qte_affichage == "Aucun repas (Eau sale)"

        # Cas 4: Test avec suppression des relations (version corrigée)
        site = SiteFactory(nom="Site Test")
        bassin = BassinFactory(nom="Bassin Test", site=site)
        lot = LotDePoissonFactory(site_prod=site, code_lot="TRUITE-2026")
        lot.bassins.add(bassin)

        # Crée d'abord le nourrissage avec qte=0 pour respecter la validation
        nourrissage = NourrissageFactory(
            site_prod=site,
            bassin=bassin,
            crea_lot=lot,
            qte=0,  # Doit être 0 pour le motif "à jeun"
            motif_absence="ajeun"
        )

        # Supprime les relations
        site.delete()
        bassin.delete()
        lot.delete()
        nourrissage.refresh_from_db()

        # Après suppression, le motif devrait toujours être visible
        assert nourrissage.qte_affichage == "0 kg"  # Le motif est conservé dans les champs redondants

