from django import forms
from .models import ReleveTempOxy, Nourrissage

class ReleveForm(forms.ModelForm):
    class Meta:
        model = ReleveTempOxy
        fields = ['site', 'temperature', 'oxygene', 'moment_jour']

class NourrissageForm(forms.ModelForm):
    class Meta:
        model = Nourrissage
        fields = [
            'site_prod',
            'bassin',
            'crea_lot',
            'aliment',
            'qte',
            'date_repas',
            'notes',
        ]
        widgets = {
            'date_repas': forms.DateInput(attrs={
                'type': 'date',          # <== important pour ton test
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # Si c’est date_repas et que type n’est pas défini, on le remet
            if name == 'date_repas' and 'type' not in field.widget.attrs:
                field.widget.attrs['type'] = 'date'

            # Ensuite on s’assure que la classe bootstrap existe
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs.update({'class': f'{existing} form-control'.strip()})
