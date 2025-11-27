from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField, Q
from apps.commun.models import TimeStampedModel
from django.core.exceptions import ValidationError
from apps.fournisseurs.models import Fournisseur

class LotDePoisson(TimeStampedModel):
    """
    Modèle représentant un lot de poissons dans la pisciculture.
    Un lot est associé à une espèce, un site de production, un fournisseur, et un ou plusieurs bassins.
    Il suit un cycle de vie (œufs, alevin, truitelle, etc.) et son poids moyen est calculé automatiquement.
    """
    STATUT_CHOICES = [
        ('OEUF', 'Œufs'),
        ('ALEVIN', 'Alevin'),
        ('TRUITELLE', 'Truitelle'),
        ('PORTION', 'Portion'),
        ('GROSSE(G)', 'Grosse'),
        ('TRES GROSSE(TG)', 'TG'),
    ]

    espece = models.ForeignKey(
        'especes.Espece',
        on_delete=models.PROTECT,
        related_name='lots',
        verbose_name="Espèce"
    )
    site_prod = models.ForeignKey(
        'sites.Site',
        on_delete=models.PROTECT,
        related_name='lots_poissons',
        verbose_name="Site de production"
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name='lot_fournis',
        verbose_name="Fournisseur"
    )
    bassins = models.ManyToManyField(
        'sites.Bassin',
        related_name='lots_poissons',
        verbose_name="Bassins"
    )
    date_arrivee = models.DateField(
        verbose_name= "Date d'arrivée",
        help_text="Date d'arrivée du lot sur site"
    )
    quantite= models.PositiveIntegerField(
        verbose_name="Quantité initiale",
        help_text="Nombre d'oeufs reçus initialement"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='OEUF',
        verbose_name="Statut"
    )
    code_lot = models.CharField(
        max_length=20,
        verbose_name="Code lot",
        help_text="Code unique identifiant d'un lot"
    )
    poids = models.FloatField(
        verbose_name="poids initial",
        help_text="Poids reçu à livraison du lot"
    )
    quantite_actuelle = models.PositiveBigIntegerField(
        verbose_name="Quantité actuelle",
        default=0,
        help_text="Quantité actuelle de poisson dans le lot"
    )
    poids_moyen = models.FloatField(
        verbose_name="Poids moyen (g)",
        blank=True,
        null=True,
        help_text="Poids moyen d'un poisson (calculé automatiquement)"
    )
    dernier_nourrissage = models.DateTimeField(
        verbose_name="Dernier nourrissage",
        null=True,
        blank=True,
        help_text="Date et heure du dernier nourrissage"
    )

    class Meta:
        verbose_name= "Lot de poissons"
        verbose_name_plural= "Lots de poissons"
        ordering = ['-date_arrivee']
        constraints = [
            models.CheckConstraint(
                check=Q(quantite__gt=0),
                name="quantite_positive"
            )
        ]
        """
        Meta:
        - constraints (list): Contraintes de validation, notamment pour garantir que la quantité est toujours positive.
        """

    def save(self, *args, **kwargs):
        """
        Sauvegarde le lot après validation des données.
        Calcule automatiquement le poids moyen (en grammes) si la quantité actuelle est supérieure à 0.
        Appelle `full_clean()` pour exécuter les validations définies dans `clean()`.
        """
        self.full_clean()
        if self.quantite_actuelle > 0:
            self.poids_moyen = round((self.poids * 1000) / self.quantite_actuelle, 2)
        else:
            self.poids_moyen = None
        super().save(*args, **kwargs)

    def clean(self):
        """
        Valide les données du lot avant sauvegarde.
        Vérifie que :
        - Aucun autre lot n'occupe les mêmes bassins.
        - La quantité initiale n'est pas égale à 0.

        Raises:
            ValidationError: Si un bassin est déjà occupé ou si la quantité est 0.
        """
        super().clean()
        # Vérifie que les bassins sélectionnés ne contiennent pas déjà un lot
        for bassin in self.bassins.all():
            # Exclut le lot actuel si c'est une mise à jour
            if LotDePoisson.objects.filter(bassins=bassin).exclude(pk=self.pk).exists():
                raise ValidationError({
                    'bassins': f"Le bassin {bassin.nom} contient déjà un lot."
                })
        if self.quantite == 0:
            raise ValidationError({"quantite": "La quantité ne peut pas être 0"})

    def __str__(self):
        """
        Retourne une représentation lisible du lot, incluant son code, l'espèce, et les quantités initiale/actuelle.

        Returns:
            str: Chaîne formatée "Code lot - Espèce (Quantité actuelle/Quantité initiale)".
            Exemple : "LOT2023 - Truite Arc en ciel (500/1000)".
        """
        return f"{self.code_lot} - {self.espece.nom_commun} ({self.quantite_actuelle}/{self.quantite})"

