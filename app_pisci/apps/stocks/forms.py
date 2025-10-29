from django import forms
from .models import LotDePoisson

class LotForm(forms.ModelForm):
    class Meta:
        model = LotDePoisson
        fields = ['espece', 'site_prod', 'fournisseur', 'bassins', 'date_arrivee', 'quantite', 'statut', 'code_lot', 'poids']
        labels = {
            'espece': 'Espèce du lot',
            'site_prod': 'Site de production',
            'fournisseur': 'Fournisseur du lot',
            'bassins': 'Bassins',
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
            'bassins': forms.SelectMultiple(attrs={'class': 'form-control'}),
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

    def clean_bassins(self):
        bassins = self.cleaned_data.get('bassins')
        if not bassins:
            return bassins  # Si aucun bassin n'est sélectionné, pas besoin de valider

        # Si c'est une création (pas d'instance existante)
        if not self.instance or not self.instance.pk:
            for bassin in bassins:
                if LotDePoisson.objects.filter(bassins=bassin).exists():
                    raise forms.ValidationError(f"Le bassin {bassin.nom} contient déjà un lot.")
        # Si c'est une mise à jour, exclure l'instance actuelle
        else:
            for bassin in bassins:
                if LotDePoisson.objects.filter(bassins=bassin).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError(f"Le bassin {bassin.nom} contient déjà un lot.")
        return bassins
