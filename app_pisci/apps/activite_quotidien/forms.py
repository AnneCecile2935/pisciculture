from django import forms
from .models import ReleveTempOxy, Nourrissage, Bassin, Aliment, LotDePoisson
from django.utils import timezone
from django.forms import formset_factory

class ReleveForm(forms.ModelForm):
    class Meta:
        model = ReleveTempOxy
        fields = ['site', 'temperature', 'oxygene', 'moment_jour']


class NourrissageForm(forms.ModelForm):
    bassin = forms.ModelChoiceField(
        queryset=Bassin.objects.none(),  # Sera défini dynamiquement dans __init__
        widget=forms.HiddenInput(),
        disabled=True,
        empty_label=None,
    )

    aliment = forms.ModelChoiceField(
        queryset=Aliment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        disabled=False,
    )
    class Meta:
        model = Nourrissage
        fields = [
            'bassin',
            'aliment',
            'qte',
            'motif_absence',
        ]
        widgets = {
            'motif_absence': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, site_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if hasattr(self, 'site_id'):
            self.fields['bassin'].queryset = Bassin.objects.filter(site_id=self.site_id)

NourrissageFormSet = formset_factory(NourrissageForm, extra=0)
