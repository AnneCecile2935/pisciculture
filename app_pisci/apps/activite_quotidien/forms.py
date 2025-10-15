from django import forms
from .models import ReleveTempOxy, Nourrissage

class ReleveForm(forms.ModelForm):
    class Meta:
        model = ReleveTempOxy
        fields = ['site', 'temperature', 'oxygene', 'moment_jour']

class NourrissageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_repas'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD'
        })

    class Meta:
        model = Nourrissage
        fields = ['site_prod', 'bassin', 'crea_lot', 'aliment', 'qte', 'date_repas', 'notes']
        