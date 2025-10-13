import pytest
from django import forms
from apps.aliments.forms import AlimentForm
from apps.fournisseurs.tests.factories import FournisseurFactory
from apps.aliments.tests.factories import AlimentFactory

@pytest.mark.django_db
class TestAlimentForm:
    def test_aliment_form_valid(self):
        """Teste un formulaire valide."""
        fournisseur = FournisseurFactory()
        form_data = {
            'nom': 'Granulés Truite',
            'code_alim': 'GRTR01',
            'description': 'Aliment complet pour truites.',
            'fournisseur': fournisseur.id
        }
        form = AlimentForm(data=form_data)
        assert form.is_valid()

    def test_aliment_form_required_fields(self):
        """Teste que les champs obligatoires sont validés."""
        form = AlimentForm(data={
            'nom': '',  # Champ obligatoire manquant
            'code_alim': '',  # Champ obligatoire manquant
            'fournisseur': FournisseurFactory().id
        })
        assert not form.is_valid()
        assert 'nom' in form.errors
        assert 'code_alim' in form.errors
        assert 'Ce champ est obligatoire' in str(form.errors)

    def test_aliment_form_widgets(self):
        """Teste que les widgets sont correctement configurés."""
        form = AlimentForm()
        assert 'form-control' in form.fields['nom'].widget.attrs['class']
        assert 'form-control' in form.fields['code_alim'].widget.attrs['class']
        assert form.fields['description'].widget.attrs['rows'] == 3
        assert form.fields['fournisseur'].empty_label == "--- Sélectionnez un fournisseur ---"

    def test_aliment_form_labels(self):
        """Teste que les labels personnalisés sont appliqués."""
        form = AlimentForm()
        assert form.fields['nom'].label == "Nom de l'aliment"
        assert form.fields['code_alim'].label == "Code (6 caractères max)"

    def test_aliment_form_help_texts(self):
        """Teste que les textes d'aide sont corrects."""
        form = AlimentForm()
        assert form.fields['nom'].help_text == "Nom complet de l'aliment (ex: Granulés Truite)."
        assert form.fields['code_alim'].help_text == "Code unique pour identifier l'aliment (6 caractères max)."

    def test_aliment_form_error_messages(self):
        """Teste les messages d'erreur personnalisés."""
        # Test pour nom unique
        fournisseur = FournisseurFactory()
        AlimentFactory(nom="Existant", code_alim="EXIST", fournisseur=fournisseur)
        form = AlimentForm(data={
            'nom': "Existant",  # Nom dupliqué
            'code_alim': 'NEW001',
            'fournisseur': fournisseur.id
        })
        assert not form.is_valid()
        assert 'Un aliment avec ce nom existe déjà' in str(form.errors['nom'])

    def test_aliment_form_placeholders(self):
        """Teste que les placeholders sont corrects."""
        form = AlimentForm()
        assert form.fields['nom'].widget.attrs['placeholder'] == "Ex: Granulés Truite"
        assert form.fields['code_alim'].widget.attrs['placeholder'] == "Ex: GRTR01"
