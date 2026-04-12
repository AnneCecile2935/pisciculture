import pytest
from apps.aliments.forms import AlimentForm
from apps.aliments.tests.factories import AlimentFactory

pytestmark = pytest.mark.django_db


def test_form_valid(fournisseur):
    form = AlimentForm(data={
        "nom": "Granulés",
        "code_alim": "GR001",
        "description": "Test",
        "fournisseur": fournisseur.id
    })

    assert form.is_valid()


def test_nom_required(fournisseur):
    form = AlimentForm(data={
        "nom": "",
        "code_alim": "GR001",
        "fournisseur": fournisseur.id
    })

    assert not form.is_valid()
    assert "nom" in form.errors


def test_code_unique(fournisseur):
    AlimentFactory(code_alim="DUP001", fournisseur=fournisseur)

    form = AlimentForm(data={
        "nom": "Autre",
        "code_alim": "DUP001",
        "fournisseur": fournisseur.id
    })

    assert not form.is_valid()
    assert "code_alim" in form.errors
