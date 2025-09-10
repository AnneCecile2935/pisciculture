from django import forms
from .models import ReleveTempOxy

class ReleveForm(forms.ModelForrm):
    class Meta:
        model = ReleveTempOxy
        fields = ['site', 'moment du jour', 'température', 'oxygène']
        widgets = {
            'température': forms.NumberInput(attrs={'step': '0.1'}),
            'oxygène': forms.NumberInput(attrs={'step': '0.1'}),
        }
