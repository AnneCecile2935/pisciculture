import pytest
from django import forms
from apps.fournisseurs.forms import FournisseurForm
from apps.fournisseurs.models import Fournisseur
from .factories import FournisseurFactory

@pytest.mark.django_db
class TestFournisseurForm:
    def test_fournisseur_form_valid(self):
        """Teste un formulaire valide avec toutes les données requises."""
        form_data = {
            'nom': 'Super Fournisseur',
            'adresse': '123 Rue des Tests',
            'ville': 'Testville',
            'code_postal': '35000',  # ← Code postal valide (5 chiffres)
            'type_fournisseur': 'ALIMENT',
            'est_actif': True,
            'contact': 'Jean Test',
            'telephone': '0123456789',
            'email': 'contact@test.com'
        }
        form = FournisseurForm(data=form_data)
        assert form.is_valid()

    def test_fournisseur_form_required_fields(self):
        """Teste que les champs obligatoires sont bien validés."""
        form = FournisseurForm(data={
            'nom': '',  # Champ obligatoire
            'adresse': '',  # Champ obligatoire
            'ville': '',  # Champ obligatoire
            'code_postal': '',  # Champ obligatoire
            'type_fournisseur': '',  # Champ obligatoire
        })
        assert not form.is_valid()
        assert 'nom' in form.errors
        assert 'adresse' in form.errors
        assert 'ville' in form.errors
        assert 'code_postal' in form.errors
        assert 'type_fournisseur' in form.errors
        # Vérifie que 'email' et 'telephone' ne sont pas obligatoires
        assert 'email' not in form.errors
        assert 'telephone' not in form.errors

    def test_fournisseur_form_optional_fields(self):
        """Teste que les champs optionnels (email, telephone) sont acceptés vides."""
        form = FournisseurForm(data={
            'nom': 'Fournisseur Minimal',
            'adresse': 'Rue Minimale',
            'ville': 'Ville Minimale',
            'code_postal': '75000',
            'type_fournisseur': 'OEUFS',
            'est_actif': False,
            'contact': '',  # Optionnel
            'telephone': '',  # Optionnel
            'email': '',  # Optionnel
        })
        assert form.is_valid()

    def test_fournisseur_form_code_postal_validation(self):
        """Teste la validation personnalisée du code postal (5 chiffres)."""
        # Code postal trop court
        form = FournisseurForm(data={
            'nom': 'Test',
            'adresse': '123 Rue',
            'ville': 'Ville',
            'code_postal': '123',  # ← Trop court
            'type_fournisseur': 'MATERIEL',
        })
        assert not form.is_valid()
        assert 'code_postal' in form.errors
        assert "5 chiffres" in form.errors['code_postal'][0]

        # Code postal avec des lettres
        form = FournisseurForm(data={
            'nom': 'Test',
            'adresse': '123 Rue',
            'ville': 'Ville',
            'code_postal': 'ABCDE',  # ← Pas des chiffres
            'type_fournisseur': 'MATERIEL',
        })
        assert not form.is_valid()
        assert "5 chiffres" in form.errors['code_postal'][0]

        # Code postal valide
        form = FournisseurForm(data={
            'nom': 'Test',
            'adresse': '123 Rue',
            'ville': 'Ville',
            'code_postal': '13000',  # ← Valide
            'type_fournisseur': 'MATERIEL',
        })
        assert form.is_valid()

    def test_fournisseur_form_widgets(self):
        """Teste que les widgets sont correctement configurés."""
        form = FournisseurForm()
        assert 'form-control' in form.fields['nom'].widget.attrs['class']
        assert 'form-control' in form.fields['adresse'].widget.attrs['class']
        assert 'form-control' in form.fields['type_fournisseur'].widget.attrs['class']
        assert 'form-check-input' in form.fields['est_actif'].widget.attrs['class']

    def test_fournisseur_form_labels(self):
        """Teste que les labels personnalisés sont appliqués."""
        form = FournisseurForm()
        assert form.fields['est_actif'].label == "Fournisseur actif"

    def test_fournisseur_form_help_texts(self):
        """Teste que les textes d'aide sont corrects."""
        form = FournisseurForm()
        assert form.fields['code_postal'].help_text == "Format attendu : 5 Chiffres (ex: 35000)"

    def test_fournisseur_form_type_fournisseur_choices(self):
        """Teste que les choix pour type_fournisseur sont limités aux options valides."""
        form = FournisseurForm()
        choices = [choice[0] for choice in form.fields['type_fournisseur'].choices]
        assert choices == ['','ALIMENT', 'OEUFS', 'MATERIEL']

    def test_fournisseur_form_save(self):
        """Teste que le formulaire enregistre correctement les données."""
        form_data = {
            'nom': 'Fournisseur Sauvegardé',
            'adresse': '123 Rue Sauvegarde',
            'ville': 'Sauvegardville',
            'code_postal': '69000',
            'type_fournisseur': 'ALIMENT',
            'est_actif': True,
            'contact': 'Contact Test',
            'telephone': '0987654321',
            'email': 'save@test.com'
        }
        form = FournisseurForm(data=form_data)
        assert form.is_valid()
        fournisseur = form.save()
        assert fournisseur.nom == 'Fournisseur Sauvegardé'
        assert fournisseur.code_postal == '69000'
        assert fournisseur.type_fournisseur == 'ALIMENT'

    def test_clean_code_postal_method(self):
    # Code postal valide
        data = {
            'nom': 'Test',
            'adresse': '123 Rue',
            'ville': 'Ville',
            'code_postal': '35000',
            'type_fournisseur': 'ALIMENT',
            'est_actif': True
        }
        form = FournisseurForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data['code_postal'] == '35000'

        # Code postal invalide (trop court)
        data['code_postal'] = '350'
        form = FournisseurForm(data=data)
        assert not form.is_valid()
        assert "5 chiffres" in form.errors['code_postal'][0]

        # Code postal invalide (lettres)
        data['code_postal'] = 'ABCDE'
        form = FournisseurForm(data=data)
        assert not form.is_valid()
        assert "5 chiffres" in form.errors['code_postal'][0]

    def test_fournisseur_form_optional_fields_explicit(self):
        """Teste que email et telephone sont bien marqués comme non obligatoires."""
        form = FournisseurForm()
        assert form.fields['email'].required is False
        assert form.fields['telephone'].required is False
