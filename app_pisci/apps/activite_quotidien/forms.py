from django import forms
from .models import ReleveTempOxy, Nourrissage, Bassin, Aliment
from django.utils import timezone

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
                'type': 'date',
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

class NourrissageParSiteForm(forms.Form):
    date_repas = forms.DateField(
        label="Date du repas",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date()
    )

    def __init__(self, *args, site_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_id = site_id

        # Récupération des bassins du site
        self.bassins = (
            Bassin.objects
            .filter(site_id=site_id)
            .distinct()
            .prefetch_related('lots_poissons')
        )

        # Création dynamique des champs par bassin
        for bassin in self.bassins:
            # Cherche le dernier aliment utilisé pour ce bassin
            dernier_nourrissage = (
                Nourrissage.objects
                .filter(bassin=bassin)
                .order_by('-date_repas')
                .first()
            )
            dernier_aliment_id = (
                dernier_nourrissage.aliment.id if dernier_nourrissage else None
            )

            # Ajout d'un attribut pour utilisation côté template/JS
            bassin.dernier_aliment_id = dernier_aliment_id

            # Champ Aliment
            self.fields[f'aliment_{bassin.id}'] = forms.ModelChoiceField(
                queryset=Aliment.objects.all(),
                initial=dernier_aliment_id,
                label=f"Aliment pour {bassin.nom}",
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )

            # Champ Quantité
            self.fields[f'qte_{bassin.id}'] = forms.DecimalField(
                label="Quantité (kg)",
                min_value=0.01,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
            )

            # Champ caché pour le bassin
            self.fields[f'bassin_{bassin.id}'] = forms.IntegerField(
                widget=forms.HiddenInput(),
                initial=bassin.id
            )

            # Champ caché pour le lot de poissons associé (s’il existe)
            lot = bassin.lots_poissons.first()
            if lot:
                self.fields[f'lot_{bassin.id}'] = forms.IntegerField(
                    widget=forms.HiddenInput(),
                    initial=lot.id
                )

        # Champ de commentaires général
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ajoutez des commentaires si nécessaire...'
            }),
            required=False,
            label="Commentaires"
        )

    def get_bassins(self):
        """Retourne la liste des bassins du site."""
        return self.bassins

    def save(self, user):
        """Crée les enregistrements de nourrissage en base."""
        date_repas = self.cleaned_data.get('date_repas')
        nourrissages = []

        for bassin in self.bassins:
            aliment_id = self.cleaned_data.get(f'aliment_{bassin.id}')
            qte = self.cleaned_data.get(f'qte_{bassin.id}')
            lot_id = self.cleaned_data.get(f'lot_{bassin.id}')

            if aliment_id and qte and lot_id:
                nourrissage = Nourrissage(
                    site_prod=bassin.site,
                    bassin=bassin,
                    crea_lot_id=lot_id if lot_id else None,
                    aliment_id=aliment_id.id if hasattr(aliment_id, 'id') else aliment_id,
                    qte=qte,
                    date_repas=date_repas,
                    cree_par=user,
                    notes=self.cleaned_data.get('notes')
                )
                nourrissages.append(nourrissage)


        return Nourrissage.objects.bulk_create(nourrissages)
