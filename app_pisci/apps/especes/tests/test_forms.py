import pytest
from django import forms
from apps.especes.forms import EspeceForm
from apps.especes.models import Espece

@pytest.mark.django_db
class TestEspeceForm:
    def test_espece_form_valid(self):
        """Teste un formulaire valide."""
        form_data = {
            'nom_commun': 'Truite Arc en ciel',
            'nom_scientifique': 'Oncorhynchus mykiss',
            'est_actif': True
        }
        form = EspeceForm(data=form_data)
        assert form.is_valid()

    def test_espece_form_required_fields(self):
        """Teste que les champs obligatoires sont validés."""
        form = EspeceForm(data={
            'nom_commun': '',  # Champ obligatoire manquant
            'nom_scientifique': '',  # Champ obligatoire manquant
            'est_actif': True
        })
        assert not form.is_valid()
        assert 'nom_commun' in form.errors
        assert 'nom_scientifique' in form.errors
        assert 'Ce champ est obligatoire.' in str(form.errors)

    def test_espece_form_widgets(self):
        """Teste que les widgets sont correctement configurés."""
        form = EspeceForm()
        # Vérifie les classes CSS
        assert 'form-control' in form.fields['nom_commun'].widget.attrs['class']
        assert 'form-control' in form.fields['nom_scientifique'].widget.attrs['class']
        assert 'form-check-input' in form.fields['est_actif'].widget.attrs['class']
        # Vérifie les placeholders
        assert form.fields['nom_commun'].widget.attrs['placeholder'] == 'Ex: Truite Arc en ciel'
        assert form.fields['nom_scientifique'].widget.attrs['placeholder'] == 'Ex: Oncorhynchus mykiss'

    def test_espece_form_labels(self):
        """Teste que les labels personnalisés sont appliqués."""
        form = EspeceForm()
        assert form.fields['est_actif'].label == "Espèce active"

    def test_espece_form_help_texts(self):
        """Teste que les textes d'aide sont corrects."""
        form = EspeceForm()
        assert form.fields['nom_commun'].help_text == "Ex: Truite Arc en ciel"
        assert form.fields['nom_scientifique'].help_text == "Ex: Oncorhynchus mykiss"

    def test_espece_form_save(self):
        """Teste que le formulaire enregistre correctement les données."""
        form_data = {
            'nom_commun': 'Nouvelle Espèce',
            'nom_scientifique': 'Nouveau scientifique',
            'est_actif': False
        }
        form = EspeceForm(data=form_data)
        assert form.is_valid()
        espece = form.save()
        assert espece.nom_commun == 'Nouvelle Espèce'
        assert espece.nom_scientifique == 'Nouveau scientifique'
        assert espece.est_actif is False

    def test_espece_form_empty_data(self):
        """Teste que le formulaire ne valide pas des données vides."""
        form = EspeceForm(data={})
        assert not form.is_valid()
        assert len(form.errors) == 2
