from django import forms
from .models import Site, Bassin

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom', 'est_actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'place_holder': 'Nom du site'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BassinForm(forms.ModelForm):
    class Meta:
        model = Bassin
        fields = ['nom', 'site', 'volume', 'type', 'est_actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du bassin'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume en m³'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type (ex: Écloserie)'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
   