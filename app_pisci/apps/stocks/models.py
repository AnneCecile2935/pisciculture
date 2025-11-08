from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField, Q
from apps.commun.models import TimeStampedModel
from django.core.exceptions import ValidationError
from apps.fournisseurs.models import Fournisseur

class LotDePoisson(TimeStampedModel):
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

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.quantite_actuelle > 0:
            self.poids_moyen = round((self.poids * 1000) / self.quantite_actuelle, 2)
        else:
            self.poids_moyen = None
        super().save(*args, **kwargs)

    def clean(self):
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
        return f"{self.code_lot} - {self.espece.nom_commun} ({self.quantite_actuelle}/{self.quantite})"

