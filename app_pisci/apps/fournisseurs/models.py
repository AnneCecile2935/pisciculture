from django.db import models
from apps.commun.models import TimeStampedModel
from django.core.exceptions import ValidationError

class Fournisseur(TimeStampedModel):
    """
    Modèle représentant un fournisseur pour la pisciculture.
    Un fournisseur peut fournir des aliments, des œufs, ou du matériel.
    Chaque fournisseur est identifié par un nom, une adresse, et un type.
    """

    TYPE_FOURNISSEUR_CHOICES= [
        ('ALIMENT', 'Aliment'),
        ('OEUFS', 'Oeufs'),
        ('MATERIEL', 'Matériel'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")
    adresse = models.TextField(verbose_name="Adresse complète")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    code_postal = models.CharField(max_length=6, verbose_name="Code Postal",  help_text="Format attendu : 5 Chiffres (ex: 35000)")
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de contact")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Adresse email")
    est_actif = models.BooleanField(default=True)
    type_fournisseur = models.CharField(
        max_length=20, choices=TYPE_FOURNISSEUR_CHOICES,
        blank=False,
        verbose_name= "Type de fournisseur",
        help_text="Catégorie principale du fournisseur"
        )

    def clean(self):
        """
        Valide les champs du fournisseur avant sauvegarde.
        Lève une ValidationError si :
        - Le téléphone dépasse 20 caractères.
        - Le type de fournisseur dépasse 20 caractères.
        """
        if self.telephone and len(self.telephone) > 20:
            raise ValidationError({'telephone': 'Assurez-vous que cette valeur comporte au plus 20 caractères.'})
        if len(self.type_fournisseur) > 20:
            raise ValidationError({'type_fournisseur': 'La valeur dépasse 20 caractères.'})

    def save(self, *args, **kwargs):
        """
        Sauvegarde le fournisseur après validation complète des champs.
        Appelle `full_clean()` pour exécuter toutes les validations définies dans `clean()`.
        """
        self.full_clean()  # Valide avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Retourne une représentation lisible du fournisseur, incluant son nom et son type.

        Returns:
            str: Chaîne formatée "Nom (Type)".
            Exemple : "Nutrition Aquacole Bretonne (Aliment)".
        """
        return f"{self.nom} ({self.get_type_fournisseur_display()})" # type: ignore

    class Meta: # type: ignore
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
        """
        Meta:
        - verbose_name (str): Nom singulier pour l'interface admin.
        - verbose_name_plural (str): Nom pluriel pour l'interface admin.
        - ordering (list): Trie les fournisseurs par `nom` dans les requêtes par défaut.
        """
