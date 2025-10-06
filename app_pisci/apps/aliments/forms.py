from django import forms
from .models import Aliment

class AlimentForm(forms.ModelForm):
    class Meta:
        model = Aliment
        fields = ["nom", "code_alim", "description", "fournisseur"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3 , "class": "forms-control"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "code_alim": forms.TextInput(attrs= {"class": "form-control"}),
            "fournisseur": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "nom": "Nom de l'aliment",
            "code_alim": "Code (6 caractères max)",
            "fournisseur": "Fournisseur",
        }
        help_texts = {
            "code_alim": "Code unique pour identifier l'aliment",
        }
