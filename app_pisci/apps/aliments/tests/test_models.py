import pytest
from django.core.exceptions import ValidationError
from apps.aliments.models import Aliment
from apps.fournisseurs.models import Fournisseur
from .factories import AlimentFactory
from apps.fournisseurs.tests.factories import FournisseurFactory

@pytest.mark.django_db
class TestAlimentModel:
    def test_aliment_creation(self):
        """Teste la création d'un aliment avec des données valides."""
        aliment = AlimentFactory(
            nom="Granulés Truite",
            code_alim="GRTR01",
            description="Aliment complet pour truites"
        )
        assert str(aliment) == "Granulés Truite (Fournisseur: Fournisseur 0)"
        assert aliment.fournisseur is not None

    def test_aliment_unique_fields(self):
        """Teste que nom et code_alim sont uniques."""
        AlimentFactory(nom="Aliment Unique", code_alim="UNIQ01")
        with pytest.raises(Exception):  # Intégrité violée
            AlimentFactory(nom="Aliment Unique", code_alim="UNIQ02")
        with pytest.raises(Exception):  # Intégrité violée
            AlimentFactory(nom="Autre Aliment", code_alim="UNIQ01")

    def test_aliment_ordering(self):
        """Teste que les aliments sont triés par code_alim."""
        AlimentFactory(code_alim="CODE02")
        AlimentFactory(code_alim="CODE01")
        aliments = Aliment.objects.all()
        assert aliments[0].code_alim == "CODE01"
        assert aliments[1].code_alim == "CODE02"

    def test_aliment_str_representation(self):
        """Teste la représentation en chaîne de caractères."""
        fournisseur = FournisseurFactory(nom="Nutrition SA")
        aliment = AlimentFactory(nom="Start Aliment", fournisseur=fournisseur)
        assert str(aliment) == "Start Aliment (Fournisseur: Nutrition SA)"

    def test_aliment_meta_options(self):
        """Teste les options Meta du modèle."""
        assert Aliment._meta.verbose_name == "Aliment"
        assert Aliment._meta.verbose_name_plural == "Aliments"
        assert Aliment._meta.ordering == ["code_alim"]

    def test_aliment_blank_description(self):
        """Teste que description peut être vide."""
        aliment = AlimentFactory(description="")
        assert aliment.description == ""

    def test_aliment_fournisseur_relation(self):
        """Teste la relation avec Fournisseur."""
        fournisseur = FournisseurFactory()
        aliment = AlimentFactory(fournisseur=fournisseur)
        assert aliment in fournisseur.aliments.all()
