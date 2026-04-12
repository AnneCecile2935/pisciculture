from django import forms
from .models import ReleveTempOxy, Nourrissage, Bassin, Aliment
from django.utils import timezone
from django.forms import formset_factory

from django import forms
from .models import Nourrissage, Aliment, Bassin


from django import forms
from django.forms import formset_factory
from .models import Nourrissage, Aliment, Bassin

class NourrissageForm(forms.ModelForm):
    """
    Formulaire métier de saisie d’un nourrissage.

    Règle métier principale :
    - Soit on saisit : aliment + quantité
    - Soit on saisit : motif d’absence (et alors quantité = 0)
    """
# Bassin affiché mais non modifiable ici (rempli depuis la vue)
    bassin = forms.ModelChoiceField(queryset=Bassin.objects.all())

    # Aliment optionnel car dépend de la logique métier (aliment OU motif)
    aliment = forms.ModelChoiceField(queryset=Aliment.objects.all(), required=False)

    # Quantité optionnelle car dépend du cas métier
    qte = forms.FloatField(required=False)

    # Motif d'absence = alternative au nourrissage classique
    motif_absence = forms.ChoiceField(
        choices=[("", "----------")] + Nourrissage.MOTIFS_ABSENCE,
        required=False
    )

    class Meta:
        model = Nourrissage

        # Champs exposés dans le formulaire utilisateur
        fields = ["bassin", "aliment", "qte", "motif_absence"]

    def __init__(self, *args, bassin_id=None, site_id=None, **kwargs):
        """
        Initialisation dynamique du formulaire :

        - site_id → filtre les bassins affichés
        - bassin_id → permet de retrouver le dernier aliment utilisé
        """

        super().__init__(*args, **kwargs)

        # Filtrage des bassins par site (multi-site support)
        if site_id:
            self.fields["bassin"].queryset = Bassin.objects.filter(site_id=site_id)

        # logique métier importante :
        # préremplir le dernier aliment utilisé dans ce bassin
        if bassin_id:
            last = (
                Nourrissage.objects
                .filter(bassin_id=bassin_id, aliment__isnull=False)
                .order_by("-date_repas")
                .first()
            )

            if last:
                self.fields["aliment"].initial = last.aliment

    def clean(self):
        """
        Validation métier centrale du formulaire.

        On applique une logique stricte :

        CAS 1 :
            aliment + quantité => OK

        CAS 2 :
            motif d’absence => OK + force qte = 0

        CAS 3 :
            rien ou incomplet => erreur
        """

        cleaned_data = super().clean()

        aliment = cleaned_data.get("aliment")
        qte = cleaned_data.get("qte")
        motif = cleaned_data.get("motif_absence")

        # -------------------------
        # CAS 1 : nourrissage normal
        # -------------------------
        if aliment and qte not in [None, ""]:
            if motif:
                raise forms.ValidationError(
                    "Vous ne pouvez pas saisir un motif ET un aliment"
                )
            return cleaned_data

        # -------------------------
        # CAS 2 : absence de nourrissage
        # -------------------------
        if motif:
            # transformation métier :
            # motif => pas d’aliment + quantité forcée à 0
            cleaned_data["qte"] = 0
            cleaned_data["aliment"] = None
            return cleaned_data

        # -------------------------
        # CAS 3 : données insuffisantes
        # -------------------------
        raise forms.ValidationError(
            "Vous devez saisir soit un aliment + quantité, soit un motif d'absence"
        )
# Formset utilisé pour gérer plusieurs bassins en une seule soumission
# (cas typique : nourrir plusieurs bassins d’un site)
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
