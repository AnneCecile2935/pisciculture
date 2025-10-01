from django import forms
from .models import Aliment

class AlimentForms(forms.ModelForm):
    class Meta :
        model = Aliment
        fields = ['nom', 'description', 'categorie', 'fournisseur']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

