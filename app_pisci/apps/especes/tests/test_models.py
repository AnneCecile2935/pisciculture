import pytest
from apps.especes.models import Espece
from .factories import EspeceFactory

@pytest.mark.django_db
class TestEspeceModel:
    def test_espece_creation(self):
        """Teste la création d'une espèce."""
        espece = EspeceFactory(
            nom_commun="Truite Arc en ciel",
            nom_scientifique="Oncorhynchus mykiss"
        )
        assert str(espece) == "Truite Arc en ciel (Oncorhynchus mykiss)"
        assert espece.est_actif is True

    def test_espece_ordering(self):
        """Teste que les espèces sont triées par nom_commun."""
        EspeceFactory(nom_commun="Zebra")
        EspeceFactory(nom_commun="Alpha")
        especies = Espece.objects.all()
        assert especies[0].nom_commun == "Alpha"
        assert especies[1].nom_commun == "Zebra"

    def test_espece_str_representation(self):
        """Teste la représentation en chaîne de caractères."""
        espece = EspeceFactory(
            nom_commun="Saumon",
            nom_scientifique="Salmo salar"
        )
        assert str(espece) == "Saumon (Salmo salar)"

    def test_espece_meta_options(self):
        """Teste les options Meta du modèle."""
        assert Espece._meta.verbose_name == "Espèce"
        assert Espece._meta.verbose_name_plural == "Espèces"
        assert Espece._meta.ordering == ['nom_commun']

    def test_espece_default_values(self):
        """Teste les valeurs par défaut."""
        espece = EspeceFactory()  
        assert espece.est_actif is True
