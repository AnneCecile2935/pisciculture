from django import forms
from .models import ReleveTempOxy, Nourrissage, Bassin, Aliment
from django.utils import timezone
from django.forms import formset_factory

class NourrissageForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'un repas (nourrissage) dans un bassin.
    Gère dynamiquement la liste des bassins en fonction du site sélectionné.
    Valide la quantité, l'aliment et le motif d'absence.

    Attributes:
        bassin (ModelChoiceField): Champ masqué et désactivé pour le bassin (défini dynamiquement par le site).
        aliment (ModelChoiceField): Liste déroulante des aliments disponibles.
    """
    bassin = forms.ModelChoiceField(
        queryset=Bassin.objects.none(),  # Sera défini dynamiquement dans __init__
        widget=forms.HiddenInput(),
        empty_label=None,
        required=True,
    )

    aliment = forms.ModelChoiceField(
        queryset=Aliment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        disabled=False,
    )

    qte = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
    )
    class Meta:
        """Configuration du formulaire lié au modèle Nourrissage."""
        model = Nourrissage
        fields = [
            'site_prod',
            'bassin',
            'crea_lot',
            'aliment',
            'qte',
            'date_repas',
            'notes',
            'motif_absence',
        ]
        widgets = {
            'date_repas': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'motif_absence': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        motif_absence = cleaned_data.get('motif_absence')
        qte = cleaned_data.get('qte')
        aliment = cleaned_data.get('aliment')

        # Si "à jeun" est sélectionné, force qte à 0
        if motif_absence == 'ajeun':
            cleaned_data['qte'] = 0  # ✅ Force la quantité à 0

        if not motif_absence and not aliment:
            self.add_error(
                'aliment',
                "L'aliment est obligatoire si aucun motif d'absence n'est indiqué."
            )
        return cleaned_data

    def __init__(self, *args, site_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_id = site_id



        if self.site_id:
            self.fields['bassin'].queryset = Bassin.objects.filter(site=self.site_id)

# Crée un FormSet pour gérer plusieurs formulaires NourrissageForm en une fois
# extra=0 : Aucun formulaire supplémentaire vide par défaut
NourrissageFormSet = formset_factory(NourrissageForm, extra=0)

class ReleveTempOxyForm(forms.ModelForm):
    """
    Formulaire pour la saisie des relevés de température, oxygène et débit.
    Inclut des validations spécifiques pour les valeurs numériques et des libellés clairs.

    Features:
        - Champs avec classes CSS 'form-control' pour Bootstrap
        - Libellés personnalisés et textes d'aide
        - Validation de la température (doit être un nombre valide)
    """
    class Meta:
        """Configuration du formulaire lié au modèle ReleveTempOxy."""
        model = ReleveTempOxy
        fields = ['date_releve', 'moment_jour', 'site', 'temperature', 'oxygene', 'debit']
        widgets = {
            # Champ de sélection pour le moment de la journée, avec style Bootstrap
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
        """
        Valide que la température est un nombre valide (positif ou négatif).

        Returns:
            float: La température validée.

        Raises:
            forms.ValidationError: Si la température n'est pas un nombre valide.
        """
        temperature = self.cleaned_data.get('temperature')

        # Si une température est saisie, vérifie qu'elle est bien un nombre
        if temperature is not None:
            # Vérifie que la température est un nombre valide (positif ou négatif)
            if not isinstance(temperature, (int, float)):
                raise forms.ValidationError("La température doit être un nombre valide.")
        return temperature
