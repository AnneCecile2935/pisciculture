from django.db import models
from apps.commun.models import TimeStampedModel
from apps.fournisseurs.models import Fournisseur
from django.core.validators import RegexValidator
import uuid

class Aliment(TimeStampedModel):
    """
    Modèle représentant un aliment utilisé pour nourrir les poissons.
    Chaque aliment est associé à un fournisseur et possède un code unique pour faciliter la gestion des stocks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50, unique=True, verbose_name="Nom de l'aliment")
    code_alim = models.CharField(max_length=6, unique=True, validators=[RegexValidator(r'^[A-Z0-9]{1,6}$')], verbose_name="Code nom de l'aliment")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Description détaillée de l'aliment")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.RESTRICT, related_name="aliments", verbose_name="Fournisseur", help_text="Fournisseur de l'aliment")

    class Meta:
        verbose_name = "Aliment"
        verbose_name_plural = "Aliments"
        ordering = ["code_alim"]

    def __str__(self):
        """
        Retourne une représentation lisible de l'aliment, incluant son nom et son fournisseur.

        Returns:
            str: Chaîne formatée "Nom (Fournisseur: nom_du_fournisseur)".
        """
        return f"{self.nom} (Fournisseur: {self.fournisseur.nom})"
