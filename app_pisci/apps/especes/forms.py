from django import forms
from .models import Espece

class EspeceForm(forms.ModelForm):
    class Meta:
        model = Espece
        fields = ['nom_commun', 'nom_scientifique', 'est_actif']
        widgets = {
            'nom_commun': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Truite Arc en ciel'
            }),
            'nom_scientifique': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Oncorhynchus mykiss'
            }),
            'est_actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'est_actif': "Espèce active",  # Label personnalisé
        }
        help_texts = {
            'nom_commun': "Ex: Truite Arc en ciel",  # Texte d'aide
            'nom_scientifique': "Ex: Oncorhynchus mykiss",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation supplémentaire si nécessaire
