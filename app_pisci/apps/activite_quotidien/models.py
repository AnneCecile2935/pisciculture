from django.db import models
from django.core.validators import MinValueValidator
from apps.commun.models import TimeStampedModel
from apps.sites.models import Site, Bassin
from apps.stocks.models import LotDePoisson
from apps.aliments.models import Aliment
from apps.users.models import User


class Nourrissage(TimeStampedModel):
    site_prod = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name="Site de production"
    )

    bassin = models.ForeignKey(
        Bassin,
        on_delete=models.CASCADE,
        verbose_name="Bassin"
    )
    crea_lot = models.ForeignKey(
        LotDePoisson,
        on_delete=models.CASCADE,
        verbose_name="Lot de poissons",
        related_name="nourrissages"
    )
    aliment = models.ForeignKey(
        Aliment,
        on_delete=models.CASCADE,
        verbose_name="Type d'aliment"
    )

    qte = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Quantité(kg)",
        validators=[MinValueValidator(0.01)]
    )
    date_repas = models.DateField(
        verbose_name="Date du repas"
    )
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Enregistré par",
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires"
    )

    class Meta:
        verbose_name = "Repas Journalier"
        db_table = 'Repas_journ'
        app_label = 'activite_quotidien'

    def __str__(self):
        return f"{self.code_lot} - {self.qte} kg le {self.date_repas}"

    @property
    def code_lot(self):
        if hasattr(self.crea_lot, 'code_lot') and self.crea_lot.code_lot:
            return self.crea_lot.code_lot
        return f"LOT-{self.crea_lot.id}"


class ReleveTempOxy(TimeStampedModel):
    MOMENT_CHOICES = [
        ('matin', 'Matin'),
        ('soir', 'Soir'),
    ]
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='releves_temp_oxy')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Température (°C)")
    oxygene = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Oxygène (mg/L)")
    moment_jour = models.CharField(max_length=5, choices=MOMENT_CHOICES, verbose_name="Moment de la journée")

    def __str__(self):
        return f"Relevé du {self.date_creation.strftime('%d/%m/%Y')} ({self.get_moment_jour_display()}) : {self.temperature}°C, {self.oxygene} mg/L ({self.site.nom})"
