import pytest
from apps.fournisseurs.models import Fournisseur
from .factories import FournisseurFactory

@pytest.mark.django_db
class TestFournisseurModel:
    def test_fournisseur_creation(self):
        fournisseur = FournisseurFactory(nom="Test Aliment", type_fournisseur="ALIMENT")
        assert str(fournisseur) == "Test Aliment (Aliment)"
        assert fournisseur.est_actif is True
        assert fournisseur.get_type_fournisseur_display() == "Aliment"

    def test_fournisseur_choices(self):
        for choice, label in Fournisseur.TYPE_FOURNISSEUR_CHOICES:
            fournisseur = FournisseurFactory(type_fournisseur=choice)
            assert fournisseur.type_fournisseur == choice
            assert fournisseur.get_type_fournisseur_display() == label

    def test_fournisseur_ordering(self):
        FournisseurFactory(nom="Zebra")
        FournisseurFactory(nom="Alpha")
        fournisseurs = Fournisseur.objects.all()
        assert fournisseurs[0].nom == "Alpha"
        assert fournisseurs[1].nom == "Zebra"

    def test_fournisseur_optional_fields(self):
        fournisseur = FournisseurFactory(contact=None, telephone=None, email=None)
        assert fournisseur.contact is None
        assert fournisseur.telephone is None
        assert fournisseur.email is None
