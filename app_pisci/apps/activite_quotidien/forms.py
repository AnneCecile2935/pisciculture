from django import forms
from .models import ReleveTempOxy, Nourrissage, Bassin, Aliment
from django.utils import timezone
from django.forms import formset_factory

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

class ReleveTempOxyForm(forms.ModelForm):
    class Meta:
        model = ReleveTempOxy
        fields = ['date_releve', 'moment_jour', 'site', 'temperature', 'oxygene', 'debit']
        widgets = {
            'moment_jour': forms.Select(choices=ReleveTempOxy.MOMENT_CHOICES, attrs={'class':'form-control'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'form-control',
            }),
            'oxygene': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'form-control',
            }),
            'debit': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'form-control',
            }),
            'date_releve': forms.DateInput(attrs={
                'type':'date'
            }),
        }
        labels = {
            'site': 'Site',
            'temperature': 'Température (°C)',
            'oxygene': 'Oxygène (mg/L)',
            'debit': 'Débit (L/min)',
            'moment_jour': 'Moment de la journée',
        }
        help_texts = {
            'temperature': 'Saisissez la température en degrés Celsius (positif ou négatif).',
            'oxygene': 'Saisissez le taux d\'oxygène en mg/L.',
            'debit': 'Saisissez le débit en litres par minute.',
        }

    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature is not None:
            # Vérifie que la température est un nombre valide (positif ou négatif)
            if not isinstance(temperature, (int, float)):
                raise forms.ValidationError("La température doit être un nombre valide.")
        return temperature
