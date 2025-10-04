from django import forms
from .models import Espece

class EspeceForm(forms.ModelForm):
    class Meta:
        model = Espece
        fields = ['nom_scientifique', 'nom_commun', 'est_actif']
