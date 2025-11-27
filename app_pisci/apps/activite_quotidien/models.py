from django.db import models
from django.core.exceptions import ValidationError
from apps.commun.models import TimeStampedModel
from apps.sites.models import Site, Bassin
from apps.stocks.models import LotDePoisson
from apps.aliments.models import Aliment
from apps.users.models import User
from django.core.validators import MinValueValidator


class Nourrissage(TimeStampedModel):
    """
    Modèle représentant un repas donné à un lot de poissons dans un bassin.
    Gère les quantités d'aliment, les motifs d'absence de repas, et les commentaires.
    """
    MOTIFS_ABSENCE = [
        ('eau_sale', 'Eau sale'),
        ('ajeun', 'À jeun'),
        ('vide', 'Vide'),
        ('maladie', 'Maladie'),
        ('autre', 'Autre (préciser en commentaire)'),
    ]

    # Clé étrangère vers le site de production
    site_prod = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name="Site de production"
    )

    # Clé étrangère vers le bassin concerné
    bassin = models.ForeignKey(
        Bassin,
        on_delete=models.CASCADE,
        verbose_name="Bassin"
    )

    # Clé étrangère vers le lot de poissons concerné
    crea_lot = models.ForeignKey(
        LotDePoisson,
        on_delete=models.CASCADE,
        verbose_name="Lot de poissons",
        related_name="nourrissages"  # Permet d'accéder aux repas d'un lot via lot.nourrissages.all()
    )

    # Clé étrangère vers le type d'aliment utilisé
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
        blank=True,
        validators=[MinValueValidator(0)]  # Empêche les valeurs négatives
    )

    # Date à laquelle le repas a été donné
    date_repas = models.DateField(
        verbose_name="Date du repas"
    )

    # Motif pour lequel aucun repas n'a été donné
    motif_absence = models.CharField(
        max_length=20,
        choices=MOTIFS_ABSENCE,
        blank=True,
        null=True,
        verbose_name="Motif d'absence de repas"
    )

    # Utilisateur ayant enregistré le repas
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Enregistré par",
    )

    # Commentaires ou précisions
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires"
    )

    class Meta:
        verbose_name = "Repas Journalier"
        db_table = 'Repas_journ' # Nom personnalisé de la table en base de données
        app_label = 'activite_quotidien'

    def clean(self):
        """
        Valide les règles métier avant sauvegarde :
        - Si aucune quantité n'est renseignée, un motif d'absence est requis.
        - Si la quantité est 0, un motif d'absence est requis.
        - Si le motif est "À jeun", la quantité doit être 0.
        """

        # Valide que si qte est None, alors motif_absence doit être renseigné
        if self.qte is None and not self.motif_absence:
            raise ValidationError(
                {"motif_absence": "Un motif d'absence est requis si aucune quantité n'est renseignée."})
        # Valide que si qte est 0, alors motif_absence doit être renseigné
        if self.qte == 0 and not self.motif_absence:
            raise ValidationError(
                {"motif_absence": "Un motif d'absence est requis si la quantité est 0."})
        if self.motif_absence == 'ajeun' and self.qte != 0:
            raise ValidationError(
                {"qte": "La quantité doit être 0 si le motif est 'À jeun'."}
            )

    def save(self, *args, **kwargs):
        """Appelle la validation avant sauvegarde."""
        self.full_clean()  # Valide avant sauvegarde
        super().save(*args, **kwargs)

    @property
    def code_lot(self):
        """
        Retourne le code du lot associé.
        Si le lot n'a pas de code, génère un code par défaut.
        """
        if hasattr(self.crea_lot, 'code_lot') and self.crea_lot.code_lot:
            return self.crea_lot.code_lot
        return f"LOT-{self.crea_lot.id}"

    @property
    def qte_affichage(self):
        """
        Retourne la quantité formatée (ex: "5 kg") ou "Aucun repas" si aucune quantité n'est renseignée.
        """
        return f"{self.qte} kg" if self.qte is not None else "Aucun repas"

    @property
    def est_a_jeun(self):
        """Retourne True si le repas est marqué comme 'à jeun'."""
        return self.motif_absence == 'ajeun'

    def __str__(self):
        """
        Représentation textuelle du repas (ex: "LOT-123 - 5 kg le 2025-11-27").
        """
        return f"{self.code_lot} - {self.qte_affichage} le {self.date_repas}"

class ReleveTempOxy(TimeStampedModel):

    """
    Modèle représentant un relevé de température, d'oxygène et de débit pour un site.
    """
    # Choix possibles pour le moment de la journée
    MOMENT_CHOICES = [
        ('matin', 'Matin'),
        ('soir', 'Soir'),
    ]

    # Clé étrangère vers le site concerné
    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        related_name='releves_temp_oxy'
    )

    # Température de l'eau en °C
    temperature = models.FloatField(
        verbose_name="Température (°C)",
        null=True,
        blank=True,
        help_text="Saisir la température en degré Celsius",
    )

    # Taux d'oxygène dans l'eau en mg/L
    oxygene = models.FloatField(
        verbose_name="Oxygène (mg/L)",
        null=True,
        blank=True,
        help_text="Saisissez le taux d'oxygène en mg/L.",
    )

    # Débit d'eau en litres par minute
    debit = models.FloatField(
        verbose_name="Débit (L/min)",
        null=True,
        blank=True,
        help_text="Saisissez le débit en litres par minute."

    )

     # Moment de la journée
    moment_jour = models.CharField(
        max_length=10,
        choices=MOMENT_CHOICES,
        verbose_name="Moment de la journée",
    )

    # Date du relevé
    date_releve = models.DateField(
        verbose_name="Date du repas",
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Représentation textuelle du relevé (ex: "Relevé du 27/11/2025 (Matin) : 15°C, 8 mg/L, 100 L/min (Site A)").
        """
        return f"Relevé du {self.date_creation.strftime('%d/%m/%Y')} ({self.get_moment_jour_display()}) : {self.temperature}°C, {self.oxygene or 'N/A'} mg/L, {self.debit or 'N/A'} L/min ({self.site.nom})"
