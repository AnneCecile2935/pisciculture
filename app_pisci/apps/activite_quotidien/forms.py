from django import forms
from .models import ReleveTempOxy

class ReleveForm(forms.ModelForm):
    class Meta:
        model = ReleveTempOxy
        fields = ['site', 'temperature', 'oxygene', 'moment_jour']
