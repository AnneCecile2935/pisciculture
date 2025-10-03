from django import forms
from .models import Fournisseurs

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseurs
        fields = [
            'nom', 'adresse', 'ville', 'code_postal',
            'telephone', 'contact', 'email', 'est_actif', 'type_fournisseur'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 'place_holder': 'Fournisseur'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control', 'place_holder':'Adresse'
            }),
            'type_fournisseur': forms.Select(attrs={
                'class': 'form-control',
                'help_text': "Sélectionnez la catégorie principale du fournisseur"
            }),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'est_actif': "Fournisseur actif",
        }
        help_text = {
            'code_postal': "Format attendu : 5 Chiffres (ex: 35000)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['telephone'].required = False

    def clean_code_postal(self):
        code_postal = self.cleaned_data['code_postal']
        if not code_postal.isdigit() or len(code_postal) != 5:
            raise forms.ValidationError("Le code postal doit contenir 5 chiffres")
        return code_postal
