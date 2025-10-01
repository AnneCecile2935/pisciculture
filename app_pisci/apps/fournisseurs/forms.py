from django import forms
from .models import Fournisseurs

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseurs
        fields = ['nom', 'adresse', 'email', 'telephone']
        labels = {
            'nom': 'Nom du fournisseur',
            'adresse': 'Adresse complète',
        }
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
