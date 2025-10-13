from django import forms
from .models import Aliment

class AlimentForm(forms.ModelForm):
    class Meta:
        model = Aliment
        fields = ["nom", "code_alim", "description", "fournisseur"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Ex: Granulés Truite"
            }),
            "code_alim": forms.TextInput(attrs={
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Ex: GRTR01"
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Description détaillée de l'aliment..."
            }),
            "fournisseur": forms.Select(attrs={
                "class": "form-control"
            }),
        }
        labels = {
            "nom": "Nom de l'aliment",
            "code_alim": "Code (6 caractères max)",
            "fournisseur": "Fournisseur",
        }
        help_texts = {
            "nom": "Nom complet de l'aliment (ex: Granulés Truite).",
            "code_alim": "Code unique pour identifier l'aliment (6 caractères max).",
            "description": "Description détaillée (optionnelle).",  # ← Ajoute
            "fournisseur": "Sélectionnez un fournisseur actif.",  # ← Ajoute
        }
        error_messages = {
            "nom": {
                "required": "Ce champ est obligatoire.",
                "unique": "Un aliment avec ce nom existe déjà.",
            },
            "code_alim": {
                "required": "Ce champ est obligatoire.",
                "unique": "Ce code est déjà utilisé.",
                "max_length": "6 caractères maximum.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation supplémentaire si nécessaire
        self.fields["fournisseur"].empty_label = "--- Sélectionnez un fournisseur ---"
