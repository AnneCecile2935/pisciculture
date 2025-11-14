from django import forms
from .models import Aliment

class AlimentForm(forms.ModelForm):
    """
    Formulaire pour la création et l'édition des aliments.

    Ce formulaire permet de :
    - Saisir les informations principales d'un aliment (nom, code, description)
    - Sélectionner un fournisseur parmi les fournisseurs actifs
    - Valider les données selon les règles métier
    - Afficher des messages d'aide et d'erreur personnalisés

    Attributes:
        Meta: Configuration du formulaire (modèle, champs, widgets, etc.)
    """
    class Meta:
        """
        Métadonnées de configuration du formulaire.

        Attributes:
            model (Model): Modèle Aliment associé au formulaire
            fields (list): Liste des champs à inclure dans le formulaire
            widgets (dict): Personnalisation des widgets de saisie
                - nom: Champ texte avec classe CSS et placeholder
                - code_alim: Champ texte pour le code unique
                - description: Zone de texte multi-lignes
                - fournisseur: Liste déroulante de sélection
            labels (dict): Étiquettes personnalisées pour chaque champ
            help_texts (dict): Textes d'aide pour chaque champ
            error_messages (dict): Messages d'erreur personnalisés
        """
        model = Aliment
        fields = ["nom", "code_alim", "description", "fournisseur"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Ex: Granulés Truite"
            }),
            "code_alim": forms.TextInput(attrs={
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Ex: GRTR01"
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",  # ← Corrige la typo
                "placeholder": "Description détaillée de l'aliment..."
            }),
            "fournisseur": forms.Select(attrs={
                "class": "form-control"
            }),
        }
        labels = {
            "nom": "Nom de l'aliment",
            "code_alim": "Code (6 caractères max)",
            "fournisseur": "Fournisseur",
        }
        help_texts = {
            "nom": "Nom complet de l'aliment (ex: Granulés Truite).",
            "code_alim": "Code unique pour identifier l'aliment (6 caractères max).",
            "description": "Description détaillée (optionnelle).",  # ← Ajoute
            "fournisseur": "Sélectionnez un fournisseur actif.",  # ← Ajoute
        }
        error_messages = {
            "nom": {
                "required": "Ce champ est obligatoire.",
                "unique": "Un aliment avec ce nom existe déjà.",
            },
            "code_alim": {
                "required": "Ce champ est obligatoire.",
                "unique": "Ce code est déjà utilisé.",
                "max_length": "6 caractères maximum.",
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire et applique des personnalisations supplémentaires.

        Args:
            *args: Arguments positionnels standard
            **kwargs: Arguments nommés standard

        Side Effects:
            - Définit un label vide personnalisé pour le champ fournisseur
            - Peut être étendu pour d'autres personnalisations
        """
        super().__init__(*args, **kwargs)
        # Personnalisation du champ fournisseur
        self.fields["fournisseur"].empty_label = "--- Sélectionnez un fournisseur ---"
