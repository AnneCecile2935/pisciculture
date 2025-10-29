from django.db import models
from django.core.exceptions import ValidationError
from apps.commun.models import TimeStampedModel
from apps.sites.models import Site, Bassin
from apps.stocks.models import LotDePoisson
from apps.aliments.models import Aliment
from apps.users.models import User
from django.core.validators import MinValueValidator


class Nourrissage(TimeStampedModel):
    MOTIFS_ABSENCE = [
        ('eau_sale', 'Eau sale'),
        ('ajeun', 'À jeun'),
        ('vide', 'Vide'),
        ('maladie', 'Maladie'),
        ('autre', 'Autre (préciser en commentaire)'),
    ]

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
        verbose_name="Type d'aliment",
        null=True,
        blank=True
    )

    qte = models.IntegerField(
        verbose_name="Quantité(kg)",
        null=True,
        blank=True
    )
    date_repas = models.DateField(
        verbose_name="Date du repas"
    )
    motif_absence = models.CharField(
        max_length=20,
        choices=MOTIFS_ABSENCE,
        blank=True,
        null=True,
        verbose_name="Motif d'absence de repas"
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

    def clean(self):
        # Valide que si qte est None, alors motif_absence doit être renseigné
        if self.qte is None and not self.motif_absence:
            raise ValidationError(
                {"motif_absence": "Un motif d'absence est requis si aucune quantité n'est renseignée."})
        # Valide que si qte est 0, alors motif_absence doit être renseigné
        if self.qte == 0 and not self.motif_absence:
            raise ValidationError(
                {"motif_absence": "Un motif d'absence est requis si la quantité est 0."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Valide avant sauvegarde
        super().save(*args, **kwargs)

    @property
    def code_lot(self):
        if hasattr(self.crea_lot, 'code_lot') and self.crea_lot.code_lot:
            return self.crea_lot.code_lot
        return f"LOT-{self.crea_lot.id}"

    @property
    def qte_affichage(self):
        """Retourne l'affichage de la quantité ou 'Aucun repas' si None"""
        return f"{self.qte} kg" if self.qte is not None else "Aucun repas"

    def __str__(self):
            return f"{self.code_lot} - {self.qte_affichage} le {self.date_repas}"

class ReleveTempOxy(TimeStampedModel):
    MOMENT_CHOICES = [
        ('matin', 'Matin'),
        ('soir', 'Soir'),
    ]
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, related_name='releves_temp_oxy')
    temperature = models.FloatField(
        verbose_name="Température (°C)",
        null=True,
        blank=True,
        help_text="Saisir la température en degré Celsius",
    )
    oxygene = models.FloatField(
        verbose_name="Oxygène (mg/L)",
        null=True,
        blank=True,
        help_text="Saisissez le taux d'oxygène en mg/L.",
    )
    debit = models.FloatField(
        verbose_name="Débit (L/min)",
        null=True,
        blank=True,
        help_text="Saisissez le débit en litres par minute."

    )
    moment_jour = models.CharField(
        max_length=10,
        choices=MOMENT_CHOICES,
        verbose_name="Moment de la journée",
    )

    def __str__(self):
        return f"Relevé du {self.date_creation.strftime('%d/%m/%Y')} ({self.get_moment_jour_display()}) : {self.temperature}°C, {self.oxygene or 'N/A'} mg/L, {self.debit or 'N/A'} L/min ({self.site.nom})"
