from django import forms
from .models import LotDePoisson

class LotForm(forms.ModelForm):
    class Meta:
        model = LotDePoisson
        fields = ['espece', 'site_prod', 'fournisseur', 'bassin', 'date_arrivee', 'quantite', 'statut', 'code_lot', 'poids']
        labels = {
            'espece': 'Espèce du lot',
            'site_prod': 'Site de production',
            'fournisseur': 'Fournisseur du lot',
            'bassin': 'Bassin',
            'date_arrivee': 'Date d’arrivée du lot',
            'quantite': 'Quantité initiale reçue',
            'poids': 'Poids total reçu (en kg)',
            'code_lot': 'Code unique du lot',
            'statut': 'Statut de croissance',
        }
        widgets = {
            'date_arrivee': forms.DateInput(attrs={'type': 'date'}),
            'code_lot': forms.TextInput(attrs={'placeholder': 'Ex: LOT2025-001'}),
            'poids': forms.NumberInput(attrs={'step': '0.01'}),
            'quantite': forms.NumberInput(attrs={'min': '1'}),
        }
        help_texts = {
            'quantite': "Doit être supérieur à 0.",
            'poids': "Poids total du lot à la livraison (en kilogrammes).",
        }

    def clean_quantite(self):
        quantite = self.cleaned_data['quantite']
        if quantite <= 0:
            raise forms.ValidationError("La quantité doit être supérieure à 0.")
        return quantite
